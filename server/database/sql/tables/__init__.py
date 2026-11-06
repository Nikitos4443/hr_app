# Import every table so Base.metadata knows about all of them before create_all().
from database.sql.tables.applications import Applications
from database.sql.tables.evaluations import Evaluations
from database.sql.tables.questions import Questions
from database.sql.tables.resume_verification import ResumeVerification
from database.sql.tables.text_verification import TextVerification
from database.sql.tables.users import Users
from database.sql.tables.vacancies import Vacancies
from database.sql.tables.video_verification import VideoVerification

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
