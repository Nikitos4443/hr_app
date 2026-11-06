from abc import ABC, abstractmethod

from hr_core.models.resume_verification_model import ResumeVerification


class IResumeVerificationRepository(ABC):
    @abstractmethod
    def create(self, entity: ResumeVerification) -> ResumeVerification: ...
