from dataclasses import dataclass


@dataclass(frozen=True)
class ChatContext:
    """Which vacancy the chat is about. Only ids and names: everything the assistant says
    about the vacancy and the company comes from the vector store (see rag.py)."""

    vacancy_id: int
    company_id: int | None
    vacancy_title: str
    company_name: str
