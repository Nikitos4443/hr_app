import asyncio
import pytest
from hr_core.models.vacancy_model import Vacancy
from langchain_core.messages import AIMessage

from modules.ai_assistant.assistant import AIAssitant
from modules.ai_assistant.intent import IntentClassifier


class FakeLLM:
    """Stub for the chat model: returns a fixed intent and records every prompt it gets."""

    def __init__(self, intent: str, answer: str = "fake answer"):
        self.intent = intent
        self.answer = answer
        self.calls: list[list] = []

    def with_structured_output(self, schema):
        llm = self

        class _Structured:
            async def ainvoke(self, messages):
                return schema(msg_intent=llm.intent)

        return _Structured()

    async def ainvoke(self, messages):
        self.calls.append(messages)
        return AIMessage(content=self.answer)


VACANCY = Vacancy(title="Python Developer", company="Acme", created_by=1)


def ask(assistant: AIAssitant, text: str, thread_id: str = "t1", vacancy=VACANCY) -> str:
    return asyncio.run(assistant.ask(thread_id, text, vacancy))


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

    ask(AIAssitant(llm=llm), "що ти вмієш?", vacancy=None)

    assert '"this job"' in system_prompt(llm)


def test_history_is_kept_per_thread():
    assistant = AIAssitant(llm=FakeLLM("Helper"))

    ask(assistant, "привіт", thread_id="a")
    ask(assistant, "ще раз", thread_id="a")
    ask(assistant, "інший чат", thread_id="b")

    def history(thread_id):
        return assistant.graph.get_state({"configurable": {"thread_id": thread_id}}).values["messages"]

    assert len(history("a")) == 4  # 2 user + 2 bot
    assert len(history("b")) == 2


def test_classifier_rejects_unknown_intent():
    with pytest.raises(ValueError):
        IntentClassifier(msg_intent="Weather")
