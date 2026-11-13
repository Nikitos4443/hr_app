import eventlet
import socketio
from fastapi import APIRouter 
from fastapi_utils.cbv import cbv

from ioc.db_deps import get_vacancies_repository
from database.init_db import get_sql_db
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")


@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.on("msg_event")
def my_message(sid, data):
    print('message ', data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

