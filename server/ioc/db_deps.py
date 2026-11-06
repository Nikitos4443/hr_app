from typing import Annotated

from fastapi import Depends
from pymongo.database import Database
from sqlalchemy.orm import Session

from config import DATABASE_PROVIDER
from database.init_db import get_mongo_db, get_sql_db
from database.mongo.repositories.MongoUsersRepository import MongoUsersRepository
from database.repository_interfaces.IApplicationsRepository import IApplicationsRepository
from database.repository_interfaces.IEvaluationsRepository import IEvaluationsRepository
from database.repository_interfaces.IQuestionsRepository import IQuestionsRepository
from database.repository_interfaces.IResumeVerificationRepository import (
    IResumeVerificationRepository,
)
from database.repository_interfaces.ITextVerificationRepository import (
    ITextVerificationRepository,
)
from database.repository_interfaces.IUsersRepository import IUsersRepository
from database.repository_interfaces.IVacanciesRepository import IVacanciesRepository
from database.repository_interfaces.IVideoVerificationRepository import (
    IVideoVerificationRepository,
)
from database.sql.repositories.SQLApplicationsRepository import SQLApplicationsRepository
from database.sql.repositories.SQLEvaluationsRepository import SQLEvaluationsRepository
from database.sql.repositories.SQLQuestionsRepository import SQLQuestionsRepository
from database.sql.repositories.SQLResumeVerificationRepository import (
    SQLResumeVerificationRepository,
)
from database.sql.repositories.SQLTextVerificationRepository import (
    SQLTextVerificationRepository,
)
from database.sql.repositories.SQLUsersRepository import SQLUsersRepository
from database.sql.repositories.SQLVacanciesRepository import SQLVacanciesRepository
from database.sql.repositories.SQLVideoVerificationRepository import (
    SQLVideoVerificationRepository,
)

SqlDbDep = Annotated[Session, Depends(get_sql_db)]
MongoDbDep = Annotated[Database, Depends(get_mongo_db)]

def _unsupported_provider(repo_name: str):
    if DATABASE_PROVIDER == 'mongo':
        return NotImplementedError(f"{repo_name} is not implemented for mongo yet")
    return ValueError(f"Unknown database provider: {DATABASE_PROVIDER}")

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

def get_vacancies_repository(sql_db: SqlDbDep) -> IVacanciesRepository:
    if DATABASE_PROVIDER == 'sql':
        return SQLVacanciesRepository(db=sql_db)
    raise _unsupported_provider("VacanciesRepository")

VacanciesRepoDep = Annotated[IVacanciesRepository, Depends(get_vacancies_repository)]


def get_applications_repository(sql_db: SqlDbDep) -> IApplicationsRepository:
    if DATABASE_PROVIDER == 'sql':
        return SQLApplicationsRepository(db=sql_db)
    raise _unsupported_provider("ApplicationsRepository")

ApplicationsRepoDep = Annotated[IApplicationsRepository, Depends(get_applications_repository)]


def get_evaluations_repository(sql_db: SqlDbDep) -> IEvaluationsRepository:
    if DATABASE_PROVIDER == 'sql':
        return SQLEvaluationsRepository(db=sql_db)
    raise _unsupported_provider("EvaluationsRepository")

EvaluationsRepoDep = Annotated[IEvaluationsRepository, Depends(get_evaluations_repository)]


def get_questions_repository(sql_db: SqlDbDep) -> IQuestionsRepository:
    if DATABASE_PROVIDER == 'sql':
        return SQLQuestionsRepository(db=sql_db)
    raise _unsupported_provider("QuestionsRepository")

QuestionsRepoDep = Annotated[IQuestionsRepository, Depends(get_questions_repository)]


def get_resume_verification_repository(sql_db: SqlDbDep) -> IResumeVerificationRepository:
    if DATABASE_PROVIDER == 'sql':
        return SQLResumeVerificationRepository(db=sql_db)
    raise _unsupported_provider("ResumeVerificationRepository")

ResumeVerificationRepoDep = Annotated[
    IResumeVerificationRepository, Depends(get_resume_verification_repository)
]


def get_video_verification_repository(sql_db: SqlDbDep) -> IVideoVerificationRepository:
    if DATABASE_PROVIDER == 'sql':
        return SQLVideoVerificationRepository(db=sql_db)
    raise _unsupported_provider("VideoVerificationRepository")

VideoVerificationRepoDep = Annotated[
    IVideoVerificationRepository, Depends(get_video_verification_repository)
]

def get_text_verification_repository(sql_db: SqlDbDep) -> ITextVerificationRepository:
    if DATABASE_PROVIDER == 'sql':
        return SQLTextVerificationRepository(db=sql_db)
    raise _unsupported_provider("TextVerificationRepository")

TextVerificationRepoDep = Annotated[
    ITextVerificationRepository, Depends(get_text_verification_repository)
]