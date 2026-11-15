from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Text, func

from hr_core.sql.base import Base


class Vacancies(Base):
    __tablename__ = "vacancies"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True, index=True)
    location = Column(String, nullable=True)
    employment_type = Column(String, nullable=True)
    experience_years_min = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    responsibilities = Column(JSON, nullable=False, default=list)
    requirements = Column(JSON, nullable=False, default=list)
    nice_to_have = Column(JSON, nullable=False, default=list)
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    salary_currency = Column(String, nullable=True)
    status = Column(String, nullable=False, default="open")
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    deadline_at = Column(DateTime(timezone=True), nullable=True)
    selection_status = Column(String, nullable=False, default="pending")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
