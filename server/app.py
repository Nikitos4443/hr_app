from fastapi import FastAPI

from modules.auth import routes as auth_routes
from modules.flow import routes as flow_routes
from database.init_db import init_db

init_db()

app = FastAPI()
app.include_router(auth_routes.router)
app.include_router(flow_routes.router)
