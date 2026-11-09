from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint, func

from hr_core.sql.base import Base


class Applications(Base):
    __tablename__ = "applications"
    __table_args__ = (
        UniqueConstraint("vacancy_id", "email", name="uq_applications_vacancy_email"),
    )

    id = Column(Integer, primary_key=True)
    vacancy_id = Column(Integer, ForeignKey("vacancies.id"), nullable=False, index=True)
    email = Column(String, nullable=False, index=True)
    full_name = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    rejection_notified_at = Column(DateTime(timezone=True), nullable=True)
