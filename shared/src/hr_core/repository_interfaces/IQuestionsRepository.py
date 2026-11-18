from abc import ABC, abstractmethod

from hr_core.models.question_model import Question


class IQuestionsRepository(ABC):
    @abstractmethod
    def create(self, entity: Question) -> Question: ...

    @abstractmethod
    def get_by_id(self, question_id: int) -> Question | None: ...

    @abstractmethod
    def list_by_vacancy(self, vacancy_id: int) -> list[Question]: ...

    @abstractmethod
    def replace_for_vacancy(self, vacancy_id: int, entities: list[Question]) -> list[Question]: ...

    @abstractmethod
    def has_answers(self, vacancy_id: int) -> bool:
        """True when a candidate already answered any question of this vacancy."""

    @abstractmethod
    def count_by_vacancies(self, vacancy_ids: list[int]) -> dict[int, int]: ...
