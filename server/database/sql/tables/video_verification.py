from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from database.sql.connection import Base


class VideoVerification(Base):
    __tablename__ = "video_verification"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False, index=True)
    status = Column(String, nullable=False, default="pending")
    s3_key = Column(String, nullable=True)
    transcription = Column(Text, nullable=True)
    processed_at = Column(DateTime(timezone=True), nullable=True)
