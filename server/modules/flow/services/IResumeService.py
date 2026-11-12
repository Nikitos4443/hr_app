from abc import ABC, abstractmethod

from modules.flow.dto.create_resume_verification_dto import CreateResumeVerificationDTO


class IResumeService(ABC):
    @abstractmethod
    async def create_resume_verification(self, dto: CreateResumeVerificationDTO): ...