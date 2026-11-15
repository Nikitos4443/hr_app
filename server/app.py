import socketio
from fastapi import FastAPI
from guard import SecurityMiddleware
from modules.ai_assistant.routes import sio
from modules.auth import routes as auth_routes
from modules.auth.guards import guard_deco
from modules.flow import routes as flow_routes

from config import security_config
from database.init_db import init_db

init_db()

fastapi_app = FastAPI()
fastapi_app.add_middleware(SecurityMiddleware, config=security_config)
fastapi_app.state.guard_decorator = guard_deco
fastapi_app.include_router(auth_routes.router)
fastapi_app.include_router(flow_routes.router)
app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app)
