from sqlalchemy.orm import Session

from hr_core.models.vacancy_model import Vacancy
from hr_core.repository_interfaces.IVacanciesRepository import IVacanciesRepository
from hr_core.sql.tables.vacancies import Vacancies


class SQLVacanciesRepository(IVacanciesRepository):
    def __init__(self, db: Session):
        super().__init__()
        self.db = db

    def create(self, entity: Vacancy) -> Vacancy:
        row = Vacancies(**entity.model_dump(exclude={"id"}, exclude_none=True))
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return Vacancy.model_validate(row)
