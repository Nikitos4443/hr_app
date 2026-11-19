from datetime import UTC, datetime

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from hr_core.models.text_verification_model import TextVerification as TextVerificationModel
from hr_core.repository_interfaces.ITextVerificationRepository import ITextVerificationRepository
from hr_core.sql.tables.applications import Applications
from hr_core.sql.tables.text_verification import TextVerification


class SQLTextVerificationRepository(ITextVerificationRepository):
    def __init__(self, db: Session):
        super().__init__()
        self.db = db

    def create(self, entity: TextVerificationModel) -> TextVerificationModel:
        row = TextVerification(**entity.model_dump(exclude={"id"}, exclude_none=True))
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return TextVerificationModel.model_validate(row)

    def save_answer(
        self, application_id: int, question_id: int, answer: str
    ) -> TextVerificationModel:
        query = select(TextVerification).where(
            TextVerification.application_id == application_id,
            TextVerification.question_id == question_id,
        )
        row = self.db.scalar(query)
        if row is None:
            row = TextVerification(application_id=application_id, question_id=question_id)
            self.db.add(row)
        row.answer = answer
        row.status = "done"
        row.processed_at = datetime.now(UTC)
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            row = self.db.scalar(query)
            row.answer = answer
            row.status = "done"
            row.processed_at = datetime.now(UTC)
            self.db.commit()
        self.db.refresh(row)
        return TextVerificationModel.model_validate(row)

    def list_by_application(self, application_id: int) -> list[TextVerificationModel]:
        rows = self.db.scalars(
            select(TextVerification).where(TextVerification.application_id == application_id)
        )
        return [TextVerificationModel.model_validate(row) for row in rows]

    def list_done_by_vacancy(self, vacancy_id: int) -> list[TextVerificationModel]:
        rows = self.db.scalars(
            select(TextVerification)
            .join(Applications, Applications.id == TextVerification.application_id)
            .where(
                Applications.vacancy_id == vacancy_id,
                Applications.status != "rejected",
                TextVerification.status == "done",
            )
        )
        return [TextVerificationModel.model_validate(row) for row in rows]

    def delete_by_application(self, application_id: int) -> None:
        self.db.execute(
            delete(TextVerification).where(TextVerification.application_id == application_id)
        )
        self.db.commit()
