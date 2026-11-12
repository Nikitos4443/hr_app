from hr_core.models.resume_verification_model import ResumeVerification
from hr_core.repository_interfaces.IResumeVerificationRepository import (
    IResumeVerificationRepository,
)
from modules.flow.dto.create_resume_verification_dto import CreateResumeVerificationDTO
from modules.flow.services.IResumeService import IResumeService


class ResumeService(IResumeService):
    def __init__(self, repo: IResumeVerificationRepository):
        self.repo = repo

    async def create_resume_verification(self, dto: CreateResumeVerificationDTO):
        resume_verification_model = ResumeVerification(
            application_id=dto.application_id,
            status="pending",
            score=None,
            llm_review=None,
            processed_at=None,
        )

        return self.repo.create(resume_verification_model)
