import asyncio

import pytest
from langchain_core.documents import Document
from langchain_core.messages import AIMessage
from modules.ai_assistant.assistant import AIAssitant
from modules.ai_assistant.chat_context import ChatContext
from modules.ai_assistant.intent import IntentClassifier

from hr_core.models.vacancy_model import Vacancy


class FakeLLM:
    """Stub for the chat model: returns a fixed intent and records every prompt it gets."""

    def __init__(self, intent: str, answer: str = "fake answer", search_query: str | None = None):
        self.intent = intent
        self.search_query = search_query
        self.answer = answer
        self.calls: list[list] = []

    def with_structured_output(self, schema):
        llm = self

        class _Structured:
            async def ainvoke(self, messages):
                return schema(msg_intent=llm.intent, search_query=llm.search_query)

        return _Structured()

    async def ainvoke(self, messages):
        self.calls.append(messages)
        return AIMessage(content=self.answer)


class FakeRetriever:
    """Stub for the vector store: returns fixed documents and records every search."""

    def __init__(self, docs: list[Document] | None = None, error: Exception | None = None):
        self.docs = docs or []
        self.error = error
        self.calls: list[tuple[str, int | None, int | None]] = []

    async def search(self, query, company_id, vacancy_id) -> list[Document]:
        self.calls.append((query, company_id, vacancy_id))
        if self.error:
            raise self.error
        return self.docs


CONTEXT = ChatContext(
    vacancy_id=3, company_id=7, vacancy_title="Python Developer", company_name="Acme"
)
VACATION_DOC = Document(
    page_content="Company document benefits.md\nEmployees get 24 paid vacation days per year.",
    metadata={"company_id": 7, "source": "benefits.md", "kind": "document"},
)
SALARY_DOC = Document(
    page_content='Vacancy "Python Developer" at Acme\nSalary: 3000-4000 USD',
    metadata={"company_id": 7, "source": "vacancy:3", "kind": "vacancy", "vacancy_id": 3},
)


def ask(assistant: AIAssitant, text: str, thread_id: str = "t1", context=CONTEXT) -> str:
    return asyncio.run(assistant.ask(thread_id, text, context))


def system_prompt(llm: FakeLLM) -> str:
    return llm.calls[-1][0].content


@pytest.mark.parametrize(
    "intent, marker",
    [
        ("Vacancy", "learn about a vacancy"),
        ("Company", "learn about the company"),
        ("Helper", "introduce yourself"),
        ("Unrelated", "not related to this job"),
    ],
)
def test_routes_to_node_by_intent(intent, marker):
    llm = FakeLLM(intent)

    assert ask(AIAssitant(llm=llm), "hi") == "fake answer"
    assert marker in system_prompt(llm)


def test_helper_prompt_mentions_vacancy_and_company():
    llm = FakeLLM("Helper")

    ask(AIAssitant(llm=llm), "хто ти?")

    prompt = system_prompt(llm)
    assert '"Python Developer"' in prompt
    assert "Acme" in prompt


def test_helper_works_without_vacancy():
    llm = FakeLLM("Helper")

    ask(AIAssitant(llm=llm), "що ти вмієш?", context=None)

    assert '"this job"' in system_prompt(llm)


def test_history_is_kept_per_thread():
    assistant = AIAssitant(llm=FakeLLM("Helper"))

    ask(assistant, "привіт", thread_id="a")
    ask(assistant, "ще раз", thread_id="a")
    ask(assistant, "інший чат", thread_id="b")

    def history(thread_id):
        return assistant.graph.get_state({"configurable": {"thread_id": thread_id}}).values[
            "messages"
        ]

    assert len(history("a")) == 4  # 2 user + 2 bot
    assert len(history("b")) == 2


def test_classifier_rejects_unknown_intent():
    with pytest.raises(ValueError):
        IntentClassifier(msg_intent="Weather")


@pytest.mark.parametrize("intent", ["Vacancy", "Company"])
def test_knowledge_is_added_to_prompt(intent):
    llm = FakeLLM(intent)
    retriever = FakeRetriever([VACATION_DOC])

    ask(AIAssitant(llm=llm, retriever=retriever), "скільки днів відпустки?")

    prompt = system_prompt(llm)
    assert "24 paid vacation days" in prompt
    assert "Company document benefits.md" in prompt
    # The search is scoped to this company and this vacancy.
    assert retriever.calls == [("скільки днів відпустки?", 7, 3)]


def test_search_uses_rewritten_query():
    llm = FakeLLM("Company", search_query="how many vacation days do employees get")
    retriever = FakeRetriever([VACATION_DOC])

    ask(AIAssitant(llm=llm, retriever=retriever), "а відпустка?")

    assert retriever.calls == [("how many vacation days do employees get", 7, 3)]


@pytest.mark.parametrize("intent", ["Helper", "Unrelated"])
def test_no_search_for_helper_and_unrelated(intent):
    retriever = FakeRetriever([VACATION_DOC])

    ask(AIAssitant(llm=FakeLLM(intent), retriever=retriever), "привіт")

    assert retriever.calls == []


def test_vacancy_facts_come_only_from_search():
    llm = FakeLLM("Vacancy")

    ask(AIAssitant(llm=llm, retriever=FakeRetriever([SALARY_DOC])), "яка зарплата?")

    prompt = system_prompt(llm)
    assert "3000-4000 USD" in prompt
    assert "<vacancy>" not in prompt
    assert "<company>" not in prompt


def test_without_retriever_prompt_says_no_information():
    llm = FakeLLM("Vacancy")

    ask(AIAssitant(llm=llm), "яка зарплата?")

    assert "No information found." in system_prompt(llm)


def test_search_error_does_not_break_chat():
    llm = FakeLLM("Company")
    retriever = FakeRetriever(error=ConnectionError("db is down"))

    answer = ask(AIAssitant(llm=llm, retriever=retriever), "яка культура?")

    assert answer == "fake answer"
    assert "No information found." in system_prompt(llm)


class FakeVacancies:
    def __init__(self, vacancy: Vacancy | None):
        self.vacancy = vacancy

    def get_by_id(self, vacancy_id):
        return self.vacancy


def test_context_has_only_ids_and_names():
    vacancy = Vacancy(
        id=3, title="Python Developer", company="Acme", company_id=7, salary_min=3000, created_by=1
    )

    assert AIAssitant.get_context(FakeVacancies(vacancy), 3) == CONTEXT
    assert AIAssitant.get_context(FakeVacancies(None), 3) is None
