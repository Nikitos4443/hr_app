

from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from config import settings
from hr_core.models.company_model import Company
from hr_core.models.vacancy_model import Vacancy
from modules.ai_assistant.intent import IntentClassifier
from modules.ai_assistant.state import State
from modules.ai_assistant.prompts import *
from modules.ai_assistant.format import *

from modules.ai_assistant.chat_context import ChatContext

from abc import ABC
from hr_core.repository_interfaces.IVacanciesRepository import IVacanciesRepository
from hr_core.repository_interfaces.ICompaniesRepository import ICompaniesRepository


class IAIAssitant(ABC):
    pass


CLASSIFIER_HISTORY = 6

class AIAssitant(IAIAssitant):
    def __init__(self, llm=None, checkpointer=None):
        self.llm = llm or init_chat_model(settings.llm_model)
        self.graph = self.build_graph(checkpointer)

    @staticmethod
    def get_context(
        vacancies: IVacanciesRepository,
        companies: ICompaniesRepository,
        vacancy_id: int,
    ) -> ChatContext | None:
        
        vacancy = vacancies.get_by_id(vacancy_id)
        if vacancy is None:
            print("No vacancy found")
            return None
        company = companies.get_by_id(vacancy.company_id) if vacancy.company_id else None
        return ChatContext(vacancy=vacancy, company=company)

    async def classify_intent(self, state: State):
        structured_llm = self.llm.with_structured_output(IntentClassifier)
        result = await structured_llm.ainvoke(
            [SystemMessage(CLASSIFIER_PROMPT), *state["messages"][-CLASSIFIER_HISTORY:]]
        )
        return {"message_intent": result.msg_intent}


    async def prompt_llm_vacancy(self, state: State):
        system = VACANCY_PROMPT.format(
            rules=BASE_RULES,
            vacancy=format_vacancy(state.get("vacancy")),
            company=format_company(state.get("company"), state.get("vacancy")),
        )
        response = await self.llm.ainvoke([SystemMessage(system), *state["messages"]])
        return {"messages": [response]}


    async def prompt_llm_company(self, state: State):
        system = COMPANY_PROMPT.format(
            rules=BASE_RULES,
            company=format_company(state.get("company"), state.get("vacancy")),
            vacancy=format_vacancy(state.get("vacancy")),
        )
        response = await self.llm.ainvoke([SystemMessage(system), *state["messages"]])
        return {"messages": [response]}


    async def prompt_llm_unrelated(self, state: State):
        vacancy = state.get("vacancy")
        system = UNRELATED_PROMPT.format(
            title=vacancy.title if vacancy else "this job",
            company=vacancy.company if vacancy else "this company",
        )
        response = await self.llm.ainvoke([SystemMessage(system), state["messages"][-1]])
        return {"messages": [response]}


    async def prompt_llm_helper(self, state: State):
        vacancy = state.get("vacancy")
        system = HELPER_PROMPT.format(
            title=vacancy.title if vacancy else "this job",
            company=vacancy.company if vacancy else "this company",
        )
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

    async def ask(self, 
        thread_id: str,
        text: str,
        vacancy: Vacancy | None,
        company: Company | None = None,
    ) -> str:
        """Один крок діалогу. thread_id — ключ історії (наприклад f"{sid}:{vacancy_id}")."""
        result = await self.graph.ainvoke(
            {
                "messages": [{"role": "user", "content": text}],
                "vacancy": vacancy,
                "company": company,
            },
            config={"configurable": {"thread_id": thread_id}},
        )
        return result["messages"][-1].text


   