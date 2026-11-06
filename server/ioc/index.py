from typing import Annotated

from fastapi import Depends
from ioc.db_deps import UsersRepoDep

from auth.AuthService import AuthService
from auth.IAuthService import IAuthService


def get_auth_service(repo: UsersRepoDep) -> IAuthService:
    return AuthService(repo=repo)

AuthServiceDep = Annotated[IAuthService, Depends(get_auth_service)]
