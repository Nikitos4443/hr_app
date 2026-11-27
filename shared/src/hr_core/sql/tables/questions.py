from sqlalchemy import Column, ForeignKey, Integer, String, Text

from hr_core.sql.base import Base


class Questions(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    vacancy_id = Column(
        Integer, ForeignKey("vacancies.id", ondelete="CASCADE"), nullable=False, index=True
    )
    order = Column(Integer, nullable=False)
    type = Column(String, nullable=False)  # video | text
    text = Column(Text, nullable=False)
    video_max_duration_sec = Column(Integer, nullable=True)
