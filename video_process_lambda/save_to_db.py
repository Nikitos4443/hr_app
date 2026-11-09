from db import SessionLocal

from hr_core.sql.repositories.SQLVideoVerificationRepository import (
    SQLVideoVerificationRepository,
)


def save_to_db(verification_id: int, text: str) -> bool:
    with SessionLocal() as session:
        repo = SQLVideoVerificationRepository(db=session)
        return repo.save_transcription(verification_id, text) is not None
