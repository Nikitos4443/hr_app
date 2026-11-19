from pydantic import BaseModel, EmailStr, Field, field_validator


class CreateApplicationDTO(BaseModel):
    vacancy_id: int
    email: EmailStr
    full_name: str | None = Field(default=None, max_length=200)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.lower()

    @field_validator("full_name")
    @classmethod
    def clean_full_name(cls, value: str | None) -> str | None:
        return (value or "").strip() or None
