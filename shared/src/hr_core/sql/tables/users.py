from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String

from hr_core.models.user_model import UserRole
from hr_core.sql.base import Base


class Users(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint(
            "role IN (" + ", ".join(f"'{r.value}'" for r in UserRole) + ")",
            name="role_valid",
        ),
    )

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    role = Column(
        String,
        nullable=False,
        default=UserRole.HR.value,
        server_default=UserRole.HR.value,
    )
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True, index=True)
