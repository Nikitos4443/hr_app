from pydantic import BaseModel, field_validator

from hr_core.models.user_model import UserRole
from modules.users.dto.create_user_dto import validate_username


class UpdateUserDTO(BaseModel):
    username: str | None = None
    password: str | None = None
    role: UserRole | None = None

    @field_validator("username")
    @classmethod
    def check_username(cls, value: str | None) -> str | None:
        return None if value is None else validate_username(value)
