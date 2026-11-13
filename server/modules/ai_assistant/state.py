from typing import Annotated, TypedDict
from hr_core.models.company_model import Company
from hr_core.models.vacancy_model import Vacancy
from langchain_core.messages import AnyMessage, SystemMessage
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    message_intent: str | None
    vacancy: Vacancy | None
    company: Company | None
