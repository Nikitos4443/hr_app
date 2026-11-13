

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



from abc import ABC, abstractmethod
from shared.src.hr_core.repository_interfaces.IVacanciesRepository import  IVacanciesRepository
class IAIAssitant(ABC):
    pass


class AIAssitant(IAIAssitant):
    def __init__(self, vacancy_repository : IVacanciesRepository):
        self.repo = vacancy_repository

    def get_by_id(self, id):
        return self.repo.get_by_id(id)
    
    
llm = init_chat_model(settings.llm_model)

CLASSIFIER_HISTORY = 6


async def classify_intent(state: State):
    structured_llm = llm.with_structured_output(IntentClassifier)
    result = await structured_llm.ainvoke(
        [SystemMessage(CLASSIFIER_PROMPT), *state["messages"][-CLASSIFIER_HISTORY:]]
    )
    return {"message_intent": result.msg_intent}


async def prompt_llm_vacancy(state: State):
    system = VACANCY_PROMPT.format(
        rules=BASE_RULES,
        vacancy=format_vacancy(state.get("vacancy")),
        company=format_company(state.get("company"), state.get("vacancy")),
    )
    response = await llm.ainvoke([SystemMessage(system), *state["messages"]])
    return {"messages": [response]}


async def prompt_llm_company(state: State):
    system = COMPANY_PROMPT.format(
        rules=BASE_RULES,
        company=format_company(state.get("company"), state.get("vacancy")),
        vacancy=format_vacancy(state.get("vacancy")),
    )
    response = await llm.ainvoke([SystemMessage(system), *state["messages"]])
    return {"messages": [response]}


async def prompt_llm_unrelated(state: State):
    vacancy = state.get("vacancy")
    system = UNRELATED_PROMPT.format(
        title=vacancy.title if vacancy else "this job",
        company=vacancy.company if vacancy else "this company",
    )
    response = await llm.ainvoke([SystemMessage(system), state["messages"][-1]])
    return {"messages": [response]}


def route_by_intent(state: State) -> str:
    return {
        "Vacancy": "vacancy_agent",
        "Company": "company_agent",
    }.get(state.get("message_intent"), "unrelated")



def build_graph(checkpointer=None):
    builder = StateGraph(State)
    builder.add_node("classifier", classify_intent)
    builder.add_node("vacancy_agent", prompt_llm_vacancy)
    builder.add_node("company_agent", prompt_llm_company)
    builder.add_node("unrelated", prompt_llm_unrelated)

    builder.add_edge(START, "classifier")
    builder.add_conditional_edges(
        "classifier",
        route_by_intent,
        ["vacancy_agent", "company_agent", "unrelated"],
    )
    builder.add_edge("vacancy_agent", END)
    builder.add_edge("company_agent", END)
    builder.add_edge("unrelated", END)

    return builder.compile(checkpointer=checkpointer or InMemorySaver())


graph = build_graph()


async def ask(
    thread_id: str,
    text: str,
    vacancy: Vacancy | None,
    company: Company | None = None,
) -> str:
    """Один крок діалогу. thread_id — ключ історії (наприклад f"{sid}:{vacancy_id}")."""
    result = await graph.ainvoke(
        {
            "messages": [{"role": "user", "content": text}],
            "vacancy": vacancy,
            "company": company,
        },
        config={"configurable": {"thread_id": thread_id}},
    )
    return result["messages"][-1].content


if __name__ == "__main__":
    import asyncio
    import uuid

    demo_vacancy = Vacancy(
        title="Python Backend Developer",
        company="Acme",
        location="Kyiv / Remote",
        employment_type="full-time",
        experience_years_min=2,
        salary_min=2000,
        salary_max=3500,
        salary_currency="USD",
        requirements=["Python 3", "FastAPI", "PostgreSQL"],
        responsibilities=["Develop REST APIs", "Code review"],
        created_by=1,
    )

    async def main():
        thread_id = str(uuid.uuid4())
        while True:
            text = input("Enter msg: ")
            print(await ask(thread_id, text, demo_vacancy))

    asyncio.run(main())
