from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import Depends, HTTPException
from starlette import status

import bcrypt
from fastapi.security import OAuth2PasswordBearer
from auth.models import User
from auth.dto.create_user_request import CreateUserRequest
from auth.database_providers import IDatabaseProvider, get_provider
from config import ACCESS_TOKEN_EXPIRE_MINUTES
import jwt
from jwt import PyJWTError
import os

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise RuntimeError('SECRET_KEY environment variable is not set')
ALGORITHM = os.getenv('ALGORITHM', 'HS256')
provider_dependency = Annotated[IDatabaseProvider, Depends(get_provider)]


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username : str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        return {'username': username, "id": user_id}
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")

def register_user(db: provider_dependency, create_user_req: CreateUserRequest):
    create_user_model = User(
        username = create_user_req.username,
        password = hash_password(create_user_req.password),
        role = 'user'
        )
    db.create_user(create_user_model)

def login(db: provider_dependency, username: str, password: str):
    user : User = authenticate_user(username, password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    token = create_access_token(user.username, user.id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {'access_token': token, 'token_type': 'bearer'}

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def authenticate_user(username: str, password: str, db: provider_dependency):
    user : User = db.query_user(username)
    if not user:
        return False
    if not bcrypt.checkpw(password.encode(), user.password.encode()):
        return False
    return user

def create_access_token(username: str, user_id : int, expires_delta: timedelta):
    encode = {'sub': username, 'id' : user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
