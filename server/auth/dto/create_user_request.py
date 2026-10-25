from pydantic import BaseModel, model_validator, field_validator
from typing_extensions import Self

class CreateUserRequest(BaseModel):
    username: str
    password: str
    confirm_password : str

    @field_validator('username')
    @classmethod
    def username_must_be_long(cls, v: str) -> str:
        if len(v) < 3:
            raise ValueError('Ім’я користувача має містити принаймні 3 символи')
        return v.lower()
    


    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError('Паролі не збігаються')
        return self