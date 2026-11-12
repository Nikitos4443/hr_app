from datetime import datetime
from typing import Any

from pydantic import BaseModel, field_validator, model_validator


class CreateResumeVerificationDTO(BaseModel):
    application_id: int
    status: str = "pending"


