from sqlalchemy.orm import Session

from database.models.vacancy_model import Vacancy
from database.repository_interfaces.IVacanciesRepository import IVacanciesRepository
from database.sql.tables.vacancies import Vacancies


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
