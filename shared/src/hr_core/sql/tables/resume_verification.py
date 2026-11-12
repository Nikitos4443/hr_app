from sqlalchemy import JSON, Column, DateTime, Float, ForeignKey, Integer, String

from hr_core.sql.base import Base


class ResumeVerification(Base):
    __tablename__ = "resume_verification"

    id = Column(Integer, primary_key=True)
    application_id = Column(
        Integer, ForeignKey("applications.id"), nullable=False, unique=True, index=True
    )
    status = Column(String, nullable=False, default="pending")
    score = Column(Float, nullable=True)
    llm_review = Column(JSON, nullable=True)
    processed_at = Column(DateTime(timezone=True), nullable=True)
