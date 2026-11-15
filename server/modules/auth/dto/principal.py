from pydantic import BaseModel

from hr_core.models.user_model import UserRole


class AuthPrincipal(BaseModel):
    id: int
    username: str
    role: UserRole
