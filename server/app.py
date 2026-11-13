from fastapi import FastAPI
from modules.ai_assistant.routes import sio
from modules.auth import routes as auth_routes
from modules.flow import routes as flow_routes
from database.init_db import init_db
import socketio
init_db()

fastapi_app = FastAPI()
fastapi_app.include_router(auth_routes.router)
fastapi_app.include_router(flow_routes.router)
app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app)


