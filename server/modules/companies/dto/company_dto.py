from pydantic import BaseModel, field_validator


def _validate_name(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError("Назва компанії не може бути порожньою")
    return value


class CreateCompanyDTO(BaseModel):
    name: str
    description: str | None = None
    website: str | None = None

    _check_name = field_validator("name")(_validate_name)


class UpdateCompanyDTO(BaseModel):
    name: str | None = None
    description: str | None = None
    website: str | None = None

    @field_validator("name")
    @classmethod
    def check_name(cls, value: str | None) -> str | None:
        return None if value is None else _validate_name(value)
