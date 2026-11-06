from abc import ABC, abstractmethod

from hr_core.models.text_verification_model import TextVerification


class ITextVerificationRepository(ABC):
    @abstractmethod
    def create(self, entity: TextVerification) -> TextVerification: ...
