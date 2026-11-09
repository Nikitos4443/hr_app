from config import MIN_CANDIDATES, SCORE_THRESHOLD
from db import SessionLocal
from output_model import OutputModel

from hr_core.models.application_model import Application
from hr_core.sql.repositories.SQLApplicationsRepository import SQLApplicationsRepository
from hr_core.sql.repositories.SQLResumeVerificationRepository import (
    SQLResumeVerificationRepository,
)


def save_to_db(
    application_id: int, vacancy_id: int, s3_key: str, result: OutputModel
) -> Application | None:
    with SessionLocal() as session:
        resumes = SQLResumeVerificationRepository(db=session)
        resumes.save_result(application_id, s3_key, result.score, result.model_dump())

        if resumes.count_active(vacancy_id) <= MIN_CANDIDATES:
            return None

        lowest = resumes.get_lowest_active_below(vacancy_id, SCORE_THRESHOLD)
        if lowest is None:
            return None

        return SQLApplicationsRepository(db=session).update_status(
            lowest.application_id, "rejected"
        )
