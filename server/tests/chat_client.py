import asyncio
import sys

import socketio

URL = "http://localhost:8000"
VACANCY_ID = 2

sio = socketio.AsyncClient()
started = asyncio.Event()
answered = asyncio.Event()


@sio.on("chat_started")
async def on_started(data):
    print(f"[чат почато] {data['title']}")
    started.set()


@sio.on("bot_typing")
async def on_typing(data=None):
    print("бот друкує...")


@sio.on("bot_message")
async def on_message(data):
    print(f"бот: {data['text']}\n")
    answered.set()


@sio.on("chat_error")
async def on_error(data):
    print(f"[помилка] {data['error']}")
    started.set()
    answered.set()


async def main():
    await sio.connect(URL)
    await sio.emit("chat_start", {"vacancy_id": VACANCY_ID})
    await started.wait()

    while True:
        text = await asyncio.to_thread(input, "ти: ")
        if text.strip() in {"exit", "quit"}:
            break
        answered.clear()
        await sio.emit("msg_event", {"text": text})
        await answered.wait()

    await sio.disconnect()


asyncio.run(main())