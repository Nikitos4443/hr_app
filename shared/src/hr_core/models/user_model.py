from pydantic import BaseModel, field_validator


class User(BaseModel):
    id: int | None = None
    username: str
    password: str
    role: str = "user"

    @field_validator("username")
    @classmethod
    def username_must_be_long(cls, v: str) -> str:
        if len(v) < 3:
            raise ValueError("Ім’я користувача має містити принаймні 3 символи")
        return v.lower()
