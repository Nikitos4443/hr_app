from sqlalchemy import JSON, Column, DateTime, Float, ForeignKey, Integer, String

from database.sql.connection import Base


class ResumeVerification(Base):
    __tablename__ = "resume_verification"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False, index=True)
    status = Column(String, nullable=False, default="pending")
    s3_key = Column(String, nullable=True)
    score = Column(Float, nullable=True)
    llm_review = Column(JSON, nullable=True)
    processed_at = Column(DateTime(timezone=True), nullable=True)
