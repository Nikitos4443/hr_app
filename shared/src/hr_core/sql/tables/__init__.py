# Import every table so Base.metadata knows about all of them before create_all().
from hr_core.sql.tables.applications import Applications
from hr_core.sql.tables.evaluations import Evaluations
from hr_core.sql.tables.questions import Questions
from hr_core.sql.tables.resume_verification import ResumeVerification
from hr_core.sql.tables.text_verification import TextVerification
from hr_core.sql.tables.users import Users
from hr_core.sql.tables.vacancies import Vacancies
from hr_core.sql.tables.video_verification import VideoVerification

__all__ = [
    "Applications",
    "Evaluations",
    "Questions",
    "ResumeVerification",
    "TextVerification",
    "Users",
    "Vacancies",
    "VideoVerification",
]
