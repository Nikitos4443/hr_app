from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from hr_core.models.vacancy_model import Vacancy
from hr_core.repository_interfaces.IVacanciesRepository import (
    IVacanciesRepository,
    VacancyHasDependenciesError,
)
from hr_core.sql.tables.vacancies import Vacancies

# Columns a vacancy owner may change; everything else (company, author, selection) is system-managed.
_UPDATABLE_FIELDS = (
    "title",
    "location",
    "employment_type",
    "experience_years_min",
    "description",
    "responsibilities",
    "requirements",
    "nice_to_have",
    "salary_min",
    "salary_max",
    "salary_currency",
    "status",
    "deadline_at",
)


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

    def get_by_id(self, vacancy_id: int) -> Vacancy | None:
        row = self.db.get(Vacancies, vacancy_id)
        return None if row is None else Vacancy.model_validate(row)

    def list_by_company(self, company_id: int) -> list[Vacancy]:
        stmt = select(Vacancies).where(Vacancies.company_id == company_id).order_by(Vacancies.id)
        return [Vacancy.model_validate(row) for row in self.db.scalars(stmt)]

    def update(self, entity: Vacancy) -> Vacancy:
        row = self.db.get(Vacancies, entity.id)
        for field in _UPDATABLE_FIELDS:
            setattr(row, field, getattr(entity, field))
        self.db.commit()
        self.db.refresh(row)
        return Vacancy.model_validate(row)

    def delete(self, vacancy_id: int) -> None:
        row = self.db.get(Vacancies, vacancy_id)
        if row is None:
            return
        try:
            self.db.delete(row)
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise VacancyHasDependenciesError from e

    def update_selection_status(self, vacancy_id: int, status: str) -> None:
        row = self.db.get(Vacancies, vacancy_id)
        if row is None:
            raise LookupError(f"vacancy {vacancy_id} not found")
        row.selection_status = status
        self.db.commit()
