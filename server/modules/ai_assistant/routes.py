"""Socket.IO chat with the AI assistant.

Client -> server:
    "chat_start" {"vacancy_id": int}  -> "chat_started" {"vacancy_id", "title"} | "chat_error"
    "msg_event"  {"text": str}        -> "bot_typing", then "bot_message" {"text"} | "chat_error"
"""

import asyncio

import socketio

from database import init_db as db
from ioc.db_deps import get_companies_repository, get_vacancies_repository
from modules.ai_assistant.assistant import AIAssitant
from modules.ai_assistant.chat_context import ChatContext

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")

assistant = AIAssitant()


def load_context(vacancy_id: int) -> ChatContext | None:
    print("loading context...")
    with db.SessionLocal() as session:
        return assistant.get_context(
            get_vacancies_repository(sql_db=session),
            get_companies_repository(sql_db=session),
            vacancy_id,
        )


@sio.event
async def connect(sid, environ, auth=None):
    print("connect", sid)


@sio.on("chat_start")
async def chat_start(sid, data):
    try:
        vacancy_id = int(data["vacancy_id"])
    except (KeyError, TypeError, ValueError):
        await sio.emit("chat_error", {"error": "vacancy_id is required"}, to=sid)
        return

    ctx = await asyncio.to_thread(load_context, vacancy_id)
    print(f"CTX: {ctx}" )
    if ctx is None:
        await sio.emit("chat_error", {"error": "Vacancy not found"}, to=sid)
        return

    await sio.save_session(sid, {"ctx": ctx, "thread_id": f"{sid}:{vacancy_id}"})
    await sio.emit("chat_started", {"vacancy_id": vacancy_id, "title": ctx.vacancy.title}, to=sid)


@sio.on("msg_event")
async def msg_event(sid, data):
    text = data.get("text", "").strip() if isinstance(data, dict) else ""
    if not text:
        await sio.emit("chat_error", {"error": "text is required"}, to=sid)
        return

    session = await sio.get_session(sid)
    ctx: ChatContext | None = session.get("ctx")
    if ctx is None:
        await sio.emit("chat_error", {"error": "Send chat_start first"}, to=sid)
        return

    await sio.emit("bot_typing", to=sid)
    try:
        answer = await assistant.ask(session["thread_id"], text, ctx.vacancy, ctx.company)
    except Exception as e:
        print("assistant error:", repr(e))
        await sio.emit("chat_error", {"error": "Assistant is unavailable"}, to=sid)
        return

    await sio.emit("bot_message", {"text": answer}, to=sid)


@sio.event
async def disconnect(sid, reason=None):
    print("disconnect", sid)
