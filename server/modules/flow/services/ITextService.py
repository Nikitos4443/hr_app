from abc import ABC, abstractmethod

from hr_core.models.application_model import Application
from hr_core.models.text_verification_model import TextVerification


class ITextService(ABC):
    @abstractmethod
    async def save_answer(
        self, application: Application, question_id: int, answer: str
    ) -> TextVerification: ...
