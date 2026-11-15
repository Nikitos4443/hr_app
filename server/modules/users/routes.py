from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from ioc.index import get_users_service
from starlette import status

from hr_core.models.user_model import UserRole
from modules.auth.guards import CurrentPrincipalDep, require_roles
from modules.users.dto.create_user_dto import CreateCompanyUserDTO
from modules.users.dto.update_user_dto import UpdateUserDTO
from modules.users.dto.user_response import UserResponse
from modules.users.IUserService import IUserService

router = APIRouter(prefix="/users", tags=["users"])


@cbv(router)
class UsersRouter:
    users_service: IUserService = Depends(get_users_service)

    @router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
    @require_roles(UserRole.COMPANY_ADMIN)
    async def create_user(self, principal: CurrentPrincipalDep, dto: CreateCompanyUserDTO):
        return self.users_service.create_company_user(principal, dto)

    @router.get("/", response_model=list[UserResponse])
    @require_roles(UserRole.COMPANY_ADMIN)
    async def list_users(self, principal: CurrentPrincipalDep):
        return self.users_service.list_users(principal)

    @router.get("/{user_id}", response_model=UserResponse)
    @require_roles(UserRole.COMPANY_ADMIN, UserRole.HR)
    async def get_user(self, user_id: int, principal: CurrentPrincipalDep):
        return self.users_service.get_user(principal, user_id)

    @router.patch("/{user_id}", response_model=UserResponse)
    @require_roles(UserRole.COMPANY_ADMIN, UserRole.HR)
    async def update_user(self, user_id: int, dto: UpdateUserDTO, principal: CurrentPrincipalDep):
        return self.users_service.update_user(principal, user_id, dto)

    @router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
    @require_roles(UserRole.COMPANY_ADMIN)
    async def delete_user(self, user_id: int, principal: CurrentPrincipalDep):
        self.users_service.delete_user(principal, user_id)
