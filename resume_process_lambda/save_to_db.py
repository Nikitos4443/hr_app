from config import MIN_CANDIDATES, SCORE_THRESHOLD
from db import SessionLocal
from output_model import OutputModel
from selection import pick_candidate_to_reject

from hr_core.sql.repositories.SQLApplicationsRepository import SQLApplicationsRepository
from hr_core.sql.repositories.SQLResumeVerificationRepository import (
    SQLResumeVerificationRepository,
)


def save_to_db(application_id: int, vacancy_id: int, s3_key: str, result: OutputModel) -> int | None:
    with SessionLocal() as session:
        resumes = SQLResumeVerificationRepository(db=session)
        resumes.save_result(application_id, s3_key, result.score, result.model_dump())

        rejected_id = pick_candidate_to_reject(
            resumes.get_active_scores(vacancy_id), MIN_CANDIDATES, SCORE_THRESHOLD
        )
        if rejected_id is not None:
            SQLApplicationsRepository(db=session).update_status(rejected_id, "rejected")
        return rejected_id
