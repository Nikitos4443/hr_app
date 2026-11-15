from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from hr_core.models.company_model import Company
from hr_core.repository_interfaces.ICompaniesRepository import (
    CompanyHasDependenciesError,
    ICompaniesRepository,
)
from hr_core.sql.tables.companies import Companies
from hr_core.sql.tables.users import Users


class SQLCompaniesRepository(ICompaniesRepository):
    def __init__(self, db: Session):
        super().__init__()
        self.db = db

    def create(self, entity: Company) -> Company:
        row = Companies(**entity.model_dump(exclude={"id"}, exclude_none=True))
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return Company.model_validate(row)

    def get_by_id(self, company_id: int) -> Company | None:
        row = self.db.get(Companies, company_id)
        return None if row is None else Company.model_validate(row)

    def get_by_name(self, name: str) -> Company | None:
        row = self.db.scalars(select(Companies).where(Companies.name == name)).first()
        return None if row is None else Company.model_validate(row)

    def update(self, entity: Company) -> Company:
        row = self.db.get(Companies, entity.id)
        row.name = entity.name
        row.description = entity.description
        row.website = entity.website
        self.db.commit()
        self.db.refresh(row)
        return Company.model_validate(row)

    def delete(self, company_id: int) -> None:
        row = self.db.get(Companies, company_id)
        if row is None:
            return
        try:
            self.db.execute(
                update(Users).where(Users.company_id == company_id).values(company_id=None)
            )
            self.db.delete(row)
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise CompanyHasDependenciesError from e
