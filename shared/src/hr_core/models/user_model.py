from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, field_validator


class UserRole(StrEnum):
    COMPANY_ADMIN = "company_admin"
    HR = "hr"


class User(BaseModel):
    id: int | None = None
    username: str
    password: str
    role: UserRole = UserRole.HR
    company_id: int | None = None
    created_at: datetime | None = None

    @field_validator("username")
    @classmethod
    def username_must_be_long(cls, v: str) -> str:
        if len(v) < 3:
            raise ValueError("Ім’я користувача має містити принаймні 3 символи")
        return v.lower()
