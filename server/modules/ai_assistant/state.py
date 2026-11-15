from typing import Annotated, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

from hr_core.models.company_model import Company
from hr_core.models.vacancy_model import Vacancy


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    message_intent: str | None
    vacancy: Vacancy | None
    company: Company | None
