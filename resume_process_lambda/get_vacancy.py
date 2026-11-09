from db import SessionLocal

from hr_core.models.vacancy_model import Vacancy
from hr_core.sql.repositories.SQLApplicationsRepository import SQLApplicationsRepository
from hr_core.sql.repositories.SQLVacanciesRepository import SQLVacanciesRepository


def get_vacancy(application_id: int) -> Vacancy:
    with SessionLocal() as session:
        application = SQLApplicationsRepository(db=session).get_by_id(application_id)
        if application is None:
            raise LookupError(f"application {application_id} not found")
        vacancy = SQLVacanciesRepository(db=session).get_by_id(application.vacancy_id)
        if vacancy is None:
            raise LookupError(f"vacancy {application.vacancy_id} not found")
        return vacancy
