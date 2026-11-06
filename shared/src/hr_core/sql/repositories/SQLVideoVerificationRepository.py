from datetime import UTC, datetime

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
