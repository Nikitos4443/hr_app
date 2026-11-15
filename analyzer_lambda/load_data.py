from candidates import Candidate, build_candidates
from db import SessionLocal

from hr_core.models.vacancy_model import Vacancy
from hr_core.sql.repositories.SQLQuestionsRepository import SQLQuestionsRepository
from hr_core.sql.repositories.SQLResumeVerificationRepository import (
    SQLResumeVerificationRepository,
)
from hr_core.sql.repositories.SQLTextVerificationRepository import SQLTextVerificationRepository
from hr_core.sql.repositories.SQLVacanciesRepository import SQLVacanciesRepository
from hr_core.sql.repositories.SQLVideoVerificationRepository import (
    SQLVideoVerificationRepository,
)


def get_vacancy(vacancy_id: int) -> Vacancy:
    with SessionLocal() as session:
        vacancy = SQLVacanciesRepository(db=session).get_by_id(vacancy_id)
        if vacancy is None:
            raise LookupError(f"vacancy {vacancy_id} not found")
        return vacancy


def set_selection_status(vacancy_id: int, status: str) -> None:
    with SessionLocal() as session:
        SQLVacanciesRepository(db=session).update_selection_status(vacancy_id, status)


def get_candidates(vacancy_id: int) -> list[Candidate]:
    with SessionLocal() as session:
        return build_candidates(
            questions=SQLQuestionsRepository(db=session).list_by_vacancy(vacancy_id),
            resumes=SQLResumeVerificationRepository(db=session).list_done_by_vacancy(vacancy_id),
            videos=SQLVideoVerificationRepository(db=session).list_done_by_vacancy(vacancy_id),
            texts=SQLTextVerificationRepository(db=session).list_done_by_vacancy(vacancy_id),
        )
