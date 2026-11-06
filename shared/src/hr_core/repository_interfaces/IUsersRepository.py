from abc import ABC, abstractmethod

from hr_core.models.user_model import User


class IUsersRepository(ABC):
    @abstractmethod
    def create_user(self, entity: User): ...

    @abstractmethod
    def query_user(self, username: str) -> User: ...
