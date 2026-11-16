import logging
from abc import ABC, abstractmethod

from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from modules.ai_assistant.chat_context import ChatContext
from modules.ai_assistant.intent import IntentClassifier
from modules.ai_assistant.prompts import (
    BASE_RULES,
    CLASSIFIER_PROMPT,
    COMPANY_PROMPT,
    HELPER_PROMPT,
    UNRELATED_PROMPT,
    VACANCY_PROMPT,
)
from modules.ai_assistant.rag import IKnowledgeRetriever, format_docs
from modules.ai_assistant.state import State

from config import settings
from hr_core.repository_interfaces.IVacanciesRepository import IVacanciesRepository


class IAIAssitant(ABC):
    @abstractmethod
    async def ask(self, thread_id: str, text: str, context: ChatContext | None) -> str: ...


CLASSIFIER_HISTORY = 6

logger = logging.getLogger(__name__)


class AIAssitant(IAIAssitant):
    def __init__(
        self,
        llm=None,
        checkpointer=None,
        retriever: IKnowledgeRetriever | None = None,
    ):
        self.llm = llm or init_chat_model(settings.llm_model)
        # All facts about the vacancy and the company come from the retriever. Without one
        # (no vector DB) the assistant can only say that the information is not available.
        self.retriever = retriever
        self.graph = self.build_graph(checkpointer)

    @staticmethod
    def get_context(vacancies: IVacanciesRepository, vacancy_id: int) -> ChatContext | None:
        """Only checks that the vacancy exists and takes the ids/names needed to scope search."""
        vacancy = vacancies.get_by_id(vacancy_id)
        if vacancy is None:
            return None
        return ChatContext(
            vacancy_id=vacancy.id,
            company_id=vacancy.company_id,
            vacancy_title=vacancy.title,
            company_name=vacancy.company,
        )

    @staticmethod
    def _names(state: State) -> dict[str, str]:
        ctx = state.get("context")
        return {
            "title": ctx.vacancy_title if ctx else "this job",
            "company": ctx.company_name if ctx else "this company",
        }

    async def classify_intent(self, state: State):
        structured_llm = self.llm.with_structured_output(IntentClassifier)
        result = await structured_llm.ainvoke(
            [SystemMessage(CLASSIFIER_PROMPT), *state["messages"][-CLASSIFIER_HISTORY:]]
        )
        return {"message_intent": result.msg_intent, "search_query": result.search_query}

    async def retrieve_knowledge(self, state: State) -> str:
        ctx = state.get("context")
        if self.retriever is None or ctx is None:
            return format_docs([])
        query = state.get("search_query") or state["messages"][-1].text
        try:
            docs = await self.retriever.search(query, ctx.company_id, ctx.vacancy_id)
        except Exception:
            # The vector DB being down must not break the chat; the model then says it
            # does not have the information.
            logger.exception("knowledge search failed")
            docs = []
        return format_docs(docs)

    async def prompt_llm_vacancy(self, state: State):
        system = VACANCY_PROMPT.format(
            rules=BASE_RULES, knowledge=await self.retrieve_knowledge(state), **self._names(state)
        )
        response = await self.llm.ainvoke([SystemMessage(system), *state["messages"]])
        return {"messages": [response]}

    async def prompt_llm_company(self, state: State):
        system = COMPANY_PROMPT.format(
            rules=BASE_RULES, knowledge=await self.retrieve_knowledge(state), **self._names(state)
        )
        response = await self.llm.ainvoke([SystemMessage(system), *state["messages"]])
        return {"messages": [response]}

    async def prompt_llm_unrelated(self, state: State):
        system = UNRELATED_PROMPT.format(**self._names(state))
        response = await self.llm.ainvoke([SystemMessage(system), state["messages"][-1]])
        return {"messages": [response]}

    async def prompt_llm_helper(self, state: State):
        system = HELPER_PROMPT.format(**self._names(state))
        response = await self.llm.ainvoke([SystemMessage(system), state["messages"][-1]])
        return {"messages": [response]}

    def route_by_intent(self, state: State) -> str:
        return {
            "Vacancy": "vacancy_agent",
            "Company": "company_agent",
            "Helper": "helper",
        }.get(state.get("message_intent"), "unrelated")

    def build_graph(self, checkpointer=None):
        builder = StateGraph(State)
        builder.add_node("classifier", self.classify_intent)
        builder.add_node("vacancy_agent", self.prompt_llm_vacancy)
        builder.add_node("company_agent", self.prompt_llm_company)
        builder.add_node("helper", self.prompt_llm_helper)
        builder.add_node("unrelated", self.prompt_llm_unrelated)

        builder.add_edge(START, "classifier")
        builder.add_conditional_edges(
            "classifier",
            self.route_by_intent,
            ["vacancy_agent", "company_agent", "helper", "unrelated"],
        )
        builder.add_edge("vacancy_agent", END)
        builder.add_edge("company_agent", END)
        builder.add_edge("helper", END)
        builder.add_edge("unrelated", END)

        return builder.compile(checkpointer=checkpointer or InMemorySaver())

    async def ask(self, thread_id: str, text: str, context: ChatContext | None) -> str:
        """Один крок діалогу. thread_id — ключ історії (наприклад f"{sid}:{vacancy_id}")."""
        result = await self.graph.ainvoke(
            {"messages": [{"role": "user", "content": text}], "context": context},
            config={"configurable": {"thread_id": thread_id}},
        )
        return result["messages"][-1].text
