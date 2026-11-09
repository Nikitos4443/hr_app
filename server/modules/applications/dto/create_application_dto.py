from pydantic import EmailStr, Field
from pydantic import BaseModel, field_validator, model_validator


class CreateApplicationDTO(BaseModel):
    vacancy_id: int
    email: EmailStr

