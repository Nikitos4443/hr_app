from pydantic import BaseModel, ConfigDict

from hr_core.models.user_model import UserRole


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    role: UserRole
    company_id: int | None
