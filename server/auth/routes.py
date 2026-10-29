from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from auth.auth import login, provider_dependency, register_user
from auth.dto.create_user_request import CreateUserRequest
from auth.dto.token import Token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Token)
async def create_user(db: provider_dependency, create_user_req: CreateUserRequest):
    register_user(db, create_user_req)
    return login(db, create_user_req.username, create_user_req.password)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: provider_dependency
):
    return login(db, form_data.username, form_data.password)
