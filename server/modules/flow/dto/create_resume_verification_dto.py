from pydantic import BaseModel


class CreateResumeVerificationDTO(BaseModel):
    application_id: int
    status: str = "pending"
