from datetime import UTC, datetime, timedelta
from typing import Annotated

import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from starlette import status

from modules.auth.dto.create_user_request import CreateUserRequest
from modules.auth.IAuthService import IAuthService
from config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from hr_core.models.user_model import User
from hr_core.repository_interfaces.IUsersRepository import IUsersRepository

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


class AuthService(IAuthService):
    def __init__(self, repo: IUsersRepository):
        self.repo = repo

    async def get_current_user(self, token: Annotated[str, Depends(oauth2_bearer)]):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            user_id: int = payload.get("id")
            if username is None or user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate user",
                )
            return {"username": username, "id": user_id}
        except PyJWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
            ) from e

    def register_user(self, create_user_req: CreateUserRequest):
        create_user_model = User(
            username=create_user_req.username,
            password=self.hash_password(create_user_req.password),
            role="user",
        )

        self.repo.create_user(create_user_model)

    def login(self, username: str, password: str):
        user: User = self.authenticate_user(username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
            )
        token = self.create_access_token(
            user.username, user.id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return {"access_token": token, "token_type": "bearer"}

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def authenticate_user(self, username: str, password: str):
        user: User = self.repo.query_user(username.lower())
        if not user:
            return False
        if not bcrypt.checkpw(password.encode(), user.password.encode()):
            return False
        return user

    def create_access_token(self, username: str, user_id: int, expires_delta: timedelta):
        encode = {"sub": username, "id": user_id}
        expires = datetime.now(UTC) + expires_delta
        encode.update({"exp": expires})
        return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
