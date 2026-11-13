from pydantic import BaseModel, EmailStr


class CreateApplicationDTO(BaseModel):
    vacancy_id: int
    email: EmailStr
