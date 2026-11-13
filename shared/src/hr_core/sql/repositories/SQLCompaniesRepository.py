from sqlalchemy.orm import Session

from hr_core.models.company_model import Company
from hr_core.repository_interfaces.ICompaniesRepository import ICompaniesRepository
from hr_core.sql.tables.companies import Companies


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
