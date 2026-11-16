from typing import Annotated, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from modules.ai_assistant.chat_context import ChatContext


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    message_intent: str | None
    search_query: str | None
    context: ChatContext | None
