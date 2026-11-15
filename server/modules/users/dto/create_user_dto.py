from pydantic import BaseModel, field_validator

from hr_core.models.user_model import UserRole


def validate_username(value: str) -> str:
    if len(value) < 3:
        raise ValueError("The name must be at least 3 symbols")
    return value.lower()


class CreateUserDTO(BaseModel):
    username: str
    password: str
    role: UserRole = UserRole.HR
    company_id: int | None = None

    _check_username = field_validator("username")(validate_username)


class CreateCompanyUserDTO(BaseModel):
    username: str
    password: str
    role: UserRole = UserRole.HR

    _check_username = field_validator("username")(validate_username)
