from abc import ABC, abstractmethod
from typing import Any

from hr_core.models.resume_verification_model import ResumeVerification


class IResumeVerificationRepository(ABC):
    @abstractmethod
    def create(self, entity: ResumeVerification) -> ResumeVerification: ...

    @abstractmethod
    def save_result(
        self, application_id: int, s3_key: str, score: float, llm_review: dict[str, Any]
    ) -> ResumeVerification: ...

    @abstractmethod
    def count_active(self, vacancy_id: int) -> int: ...

    @abstractmethod
    def get_lowest_active_below(
        self, vacancy_id: int, threshold: float
    ) -> ResumeVerification | None: ...
