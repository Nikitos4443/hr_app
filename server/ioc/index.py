from typing import Annotated, Generator

from fastapi import Depends
from pymongo.database import Database
from sqlalchemy.orm import Session

from auth.AuthService import AuthService
from auth.IAuthService import IAuthService
from config import DATABASE_PROVIDER
from database.init_db import get_mongo_db, get_sql_db
from database.mongo.repositories.MongoUsersRepository import MongoUsersRepository
from database.repository_interfaces.IUsersRepository import IUsersRepository
from database.sql.repositories.SQLUsersRepository import SQLUsersRepository

SqlDbDep = Annotated[Session, Depends(get_sql_db)]
MongoDbDep = Annotated[Database, Depends(get_mongo_db)]

def get_users_repository(
    sql_db: SqlDbDep,
    mongo_db: MongoDbDep
) -> IUsersRepository:
    if DATABASE_PROVIDER == 'sql':
        return SQLUsersRepository(db=sql_db)

    if DATABASE_PROVIDER == 'mongo':
        return MongoUsersRepository(db=mongo_db)

    raise ValueError(f"Unknown database provider: {DATABASE_PROVIDER}")

UsersRepoDep = Annotated[IUsersRepository, Depends(get_users_repository)]

def get_auth_service(repo: UsersRepoDep) -> IAuthService:
    return AuthService(repo=repo)

AuthServiceDep = Annotated[IAuthService, Depends(get_auth_service)]
