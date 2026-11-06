from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from ioc.index import AuthServiceDep
from starlette import status

from auth.dto.create_user_request import CreateUserRequest
from auth.dto.token import Token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Token)
async def create_user(
    create_user_req: CreateUserRequest,
    auth_service: AuthServiceDep,
):
    auth_service.register_user(create_user_req)
    return auth_service.login(create_user_req.username, create_user_req.password)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthServiceDep,
):
    return auth_service.login(form_data.username, form_data.password)
