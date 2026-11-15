from abc import ABC, abstractmethod

from hr_core.models.user_model import User
from modules.auth.dto.principal import AuthPrincipal
from modules.users.dto.create_user_dto import CreateCompanyUserDTO, CreateUserDTO
from modules.users.dto.update_user_dto import UpdateUserDTO


class IUserService(ABC):
    @abstractmethod
    def create_user(self, dto: CreateUserDTO) -> User: ...

    @abstractmethod
    def get_by_id(self, user_id: int) -> User | None: ...

    @abstractmethod
    def list_company_members(self, company_id: int) -> list[User]: ...

    @abstractmethod
    def set_company(self, user_id: int, company_id: int | None) -> User: ...

    @abstractmethod
    def get_by_username(self, username: str) -> User | None: ...

    @abstractmethod
    def create_company_user(self, actor: AuthPrincipal, dto: CreateCompanyUserDTO) -> User: ...

    @abstractmethod
    def list_users(self, actor: AuthPrincipal) -> list[User]: ...

    @abstractmethod
    def get_user(self, actor: AuthPrincipal, user_id: int) -> User: ...

    @abstractmethod
    def update_user(self, actor: AuthPrincipal, user_id: int, dto: UpdateUserDTO) -> User: ...

    @abstractmethod
    def delete_user(self, actor: AuthPrincipal, user_id: int) -> None: ...
