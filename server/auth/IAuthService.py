from abc import ABC

from auth.dto.create_user_request import CreateUserRequest


class IAuthService(ABC):
    async def get_current_user(self):
        pass

    def register_user(self, create_user_req: CreateUserRequest):
        pass

    def login(self, username: str, password: str):
        pass