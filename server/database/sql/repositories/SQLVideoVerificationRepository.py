from sqlalchemy.orm import Session

from database.models.video_verification_model import VideoVerification as VideoVerificationModel
from database.repository_interfaces.IVideoVerificationRepository import IVideoVerificationRepository
from database.sql.tables.video_verification import VideoVerification


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
