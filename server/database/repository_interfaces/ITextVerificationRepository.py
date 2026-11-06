from abc import ABC, abstractmethod

from database.models.text_verification_model import TextVerification


class ITextVerificationRepository(ABC):
    @abstractmethod
    def create(self, entity: TextVerification) -> TextVerification: ...
