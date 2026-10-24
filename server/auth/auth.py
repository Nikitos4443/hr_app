from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette import status

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from auth.dto.create_user_request import CreateUserRequest
from auth.models import User
from auth.database_providers import IDatabaseProvider, get_provider
from config import SECRET_KEY, ALGORITHM

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


provider_dependency = Annotated[IDatabaseProvider, Depends(get_provider)]

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(db: provider_dependency, create_user_req: CreateUserRequest):
    create_user_model = User(
        username = create_user_req.username,
        password = bcrypt_context.hash(create_user_req.password),
        role = 'user'
        )
    db.create_user(create_user_model)
