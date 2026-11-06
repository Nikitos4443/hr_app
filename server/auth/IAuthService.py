from abc import ABC, abstractmethod

from auth.dto.create_user_request import CreateUserRequest


class IAuthService(ABC):
    @abstractmethod
    async def get_current_user(self, token: str): ...

    @abstractmethod
    def register_user(self, create_user_req: CreateUserRequest): ...

    @abstractmethod
    def login(self, username: str, password: str): ...
