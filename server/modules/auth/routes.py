from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.cbv import cbv
from ioc.index import get_auth_service
from starlette import status

from modules.auth.dto.create_user_request import CreateUserRequest
from modules.auth.dto.token import Token
from modules.auth.IAuthService import IAuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@cbv(router)
class AuthRouter:
    auth_service: IAuthService = Depends(get_auth_service)

    @router.post("/", status_code=status.HTTP_201_CREATED, response_model=Token)
    async def create_user(self, create_user_req: CreateUserRequest):
        self.auth_service.register_user(create_user_req)
        return self.auth_service.login(create_user_req.username, create_user_req.password)

    @router.post("/token", response_model=Token)
    async def login_for_access_token(
        self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    ):
        return self.auth_service.login(form_data.username, form_data.password)
