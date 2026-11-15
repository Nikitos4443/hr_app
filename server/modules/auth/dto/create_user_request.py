from typing import Self

from pydantic import BaseModel, field_validator, model_validator

from hr_core.models.user_model import UserRole


class CreateUserRequest(BaseModel):
    username: str
    password: str
    confirm_password: str
    role: UserRole = UserRole.HR
    company_id: int | None = None

    @field_validator("username")
    @classmethod
    def username_must_be_long(cls, v: str) -> str:
        if len(v) < 3:
            raise ValueError("Ім’я користувача має містити принаймні 3 символи")
        return v.lower()

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError("Паролі не збігаються")
        return self
