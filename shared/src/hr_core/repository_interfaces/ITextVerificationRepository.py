from abc import ABC, abstractmethod

from hr_core.models.text_verification_model import TextVerification


class ITextVerificationRepository(ABC):
    @abstractmethod
    def create(self, entity: TextVerification) -> TextVerification: ...

    @abstractmethod
    def save_answer(
        self, application_id: int, question_id: int, answer: str
    ) -> TextVerification: ...

    @abstractmethod
    def list_done_by_vacancy(self, vacancy_id: int) -> list[TextVerification]: ...

    @abstractmethod
    def delete_by_application(self, application_id: int) -> None: ...

    @abstractmethod
    def list_by_application(self, application_id: int) -> list[TextVerification]: ...
