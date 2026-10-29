from abc import ABC, abstractmethod

from ..models import User


class IDatabaseProvider(ABC):
    @abstractmethod
    def create_user(self, entity: User): ...

    @abstractmethod
    def query_user(self, username: str) -> User: ...
