from db import SessionLocal

from hr_core.sql.repositories.SQLVideoVerificationRepository import (
    SQLVideoVerificationRepository,
)


def save_to_db(verification_id: int, text: str) -> None:
    with SessionLocal() as session:
        repo = SQLVideoVerificationRepository(db=session)
        if repo.save_transcription(verification_id, text) is None:
            raise LookupError(f"video_verification {verification_id} not found")
