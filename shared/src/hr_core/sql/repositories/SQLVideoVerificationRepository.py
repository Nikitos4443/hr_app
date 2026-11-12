from datetime import UTC, datetime

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from hr_core.models.video_verification_model import VideoVerification as VideoVerificationModel
from hr_core.repository_interfaces.IVideoVerificationRepository import IVideoVerificationRepository
from hr_core.sql.tables.video_verification import VideoVerification


class SQLVideoVerificationRepository(IVideoVerificationRepository):
    def __init__(self, db: Session):
        super().__init__()
        self.db = db

    def create(self, entity: VideoVerificationModel) -> VideoVerificationModel:
        row = VideoVerification(**entity.model_dump(exclude={"id"}, exclude_none=True))
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return VideoVerificationModel.model_validate(row)

    def get_or_create(self, application_id: int, question_id: int) -> VideoVerificationModel:
        query = select(VideoVerification).where(
            VideoVerification.application_id == application_id,
            VideoVerification.question_id == question_id,
        )
        row = self.db.scalar(query)
        if row is None:
            try:
                row = VideoVerification(
                    application_id=application_id, question_id=question_id, status="pending"
                )
                self.db.add(row)
                self.db.commit()
            except IntegrityError:
                self.db.rollback()
                row = self.db.scalar(query)
        self.db.refresh(row)
        return VideoVerificationModel.model_validate(row)

    def save_transcription(
        self, verification_id: int, transcription: str
    ) -> VideoVerificationModel | None:
        row = self.db.get(VideoVerification, verification_id)
        if row is None:
            return None
        row.transcription = transcription
        row.status = "done"
        row.processed_at = datetime.now(UTC)
        self.db.commit()
        self.db.refresh(row)
        return VideoVerificationModel.model_validate(row)

    def list_by_application(self, application_id: int) -> list[VideoVerificationModel]:
        rows = self.db.scalars(
            select(VideoVerification).where(VideoVerification.application_id == application_id)
        )
        return [VideoVerificationModel.model_validate(row) for row in rows]

    def delete_by_application(self, application_id: int) -> None:
        self.db.execute(
            delete(VideoVerification).where(VideoVerification.application_id == application_id)
        )
        self.db.commit()
