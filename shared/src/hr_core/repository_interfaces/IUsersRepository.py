from abc import ABC, abstractmethod

from hr_core.models.user_model import User


class UserHasDependenciesError(Exception):
    """The user is still referenced by other records (e.g. vacancies) and cannot be deleted."""


class IUsersRepository(ABC):
    @abstractmethod
    def create_user(self, entity: User) -> User: ...

    @abstractmethod
    def query_user(self, username: str) -> User | None: ...

    @abstractmethod
    def get_by_id(self, user_id: int) -> User | None: ...

    @abstractmethod
    def list_by_company(self, company_id: int) -> list[User]: ...

    @abstractmethod
    def update_user(self, entity: User) -> User: ...

    @abstractmethod
    def delete_user(self, user_id: int) -> None: ...
