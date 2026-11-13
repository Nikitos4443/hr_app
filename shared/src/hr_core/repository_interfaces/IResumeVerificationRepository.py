from abc import ABC, abstractmethod
from typing import Any

from hr_core.models.resume_verification_model import ResumeVerification


class IResumeVerificationRepository(ABC):
    @abstractmethod
    def create(self, entity: ResumeVerification) -> ResumeVerification: ...

    @abstractmethod
    def save_result(
        self, application_id: int, score: float, llm_review: dict[str, Any]
    ) -> ResumeVerification: ...

    @abstractmethod
    def get_active_scores(self, vacancy_id: int) -> dict[int, float]: ...

    @abstractmethod
    def list_done_by_vacancy(self, vacancy_id: int) -> list[ResumeVerification]: ...

    @abstractmethod
    def get_by_application(self, application_id: int) -> ResumeVerification | None: ...

    @abstractmethod
    def delete_by_application(self, application_id: int) -> None: ...
