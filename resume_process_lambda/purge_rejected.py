from config import settings
from db import SessionLocal

from hr_core.s3.service import S3Service
from hr_core.services.CandidateCleanupService import CandidateCleanupService
from hr_core.sql.repositories.SQLApplicationsRepository import SQLApplicationsRepository
from hr_core.sql.repositories.SQLEvaluationsRepository import SQLEvaluationsRepository
from hr_core.sql.repositories.SQLResumeVerificationRepository import (
    SQLResumeVerificationRepository,
)
from hr_core.sql.repositories.SQLTextVerificationRepository import (
    SQLTextVerificationRepository,
)
from hr_core.sql.repositories.SQLVideoVerificationRepository import (
    SQLVideoVerificationRepository,
)


def purge_rejected(vacancy_id: int) -> list[int]:
    with SessionLocal() as session:
        applications = SQLApplicationsRepository(db=session)
        cleanup = CandidateCleanupService(
            applications=applications,
            resumes=SQLResumeVerificationRepository(db=session),
            videos=SQLVideoVerificationRepository(db=session),
            texts=SQLTextVerificationRepository(db=session),
            evaluations=SQLEvaluationsRepository(db=session),
            s3=S3Service(),
            bucket_name=settings.bucket_name,
        )
        purged = []
        for application in applications.get_rejected_not_purged(vacancy_id):
            cleanup.purge(application.id)
            purged.append(application.id)
        return purged
