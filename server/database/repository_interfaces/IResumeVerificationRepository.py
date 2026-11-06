from abc import ABC, abstractmethod

from database.models.resume_verification_model import ResumeVerification


class IResumeVerificationRepository(ABC):
    @abstractmethod
    def create(self, entity: ResumeVerification) -> ResumeVerification: ...
