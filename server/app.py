from fastapi import FastAPI

from auth import routes as auth_routes
from database.init_db import init_db

init_db()

app = FastAPI()
app.include_router(auth_routes.router)
