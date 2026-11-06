from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func

from hr_core.sql.base import Base


class Evaluations(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False, unique=True)
    vacancy_id = Column(Integer, ForeignKey("vacancies.id"), nullable=False, index=True)
    order = Column(Integer, nullable=True)
    summary = Column(Text, nullable=True)
    evaluated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
