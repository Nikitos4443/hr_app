from sqlalchemy.orm import Session

from hr_core.models.application_model import Application
from hr_core.repository_interfaces.IApplicationsRepository import IApplicationsRepository
from hr_core.sql.tables.applications import Applications


class SQLApplicationsRepository(IApplicationsRepository):
    def __init__(self, db: Session):
        super().__init__()
        self.db = db

    def create(self, entity: Application) -> Application:
        row = Applications(**entity.model_dump(exclude={"id"}, exclude_none=True))
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return Application.model_validate(row)
