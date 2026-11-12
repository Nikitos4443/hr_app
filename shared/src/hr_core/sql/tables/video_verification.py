from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint

from hr_core.sql.base import Base


class VideoVerification(Base):
    __tablename__ = "video_verification"
    __table_args__ = (
        UniqueConstraint(
            "application_id", "question_id", name="uq_video_verification_application_question"
        ),
    )

    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False, index=True)
    status = Column(String, nullable=False, default="pending")
    transcription = Column(Text, nullable=True)
    processed_at = Column(DateTime(timezone=True), nullable=True)
