from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from hr_core.sql.base import Base


class TextVerification(Base):
    __tablename__ = "text_verification"

    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False, index=True)
    status = Column(String, nullable=False, default="pending")
    answer = Column(Text, nullable=True)
    processed_at = Column(DateTime(timezone=True), nullable=True)
