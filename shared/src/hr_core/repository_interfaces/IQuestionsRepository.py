from abc import ABC, abstractmethod

from hr_core.models.question_model import Question


class IQuestionsRepository(ABC):
    @abstractmethod
    def create(self, entity: Question) -> Question: ...

    @abstractmethod
    def get_by_id(self, question_id: int) -> Question | None: ...

    @abstractmethod
    def list_by_vacancy(self, vacancy_id: int) -> list[Question]: ...
