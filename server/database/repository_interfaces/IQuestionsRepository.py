from abc import ABC, abstractmethod

from database.models.question_model import Question


class IQuestionsRepository(ABC):
    @abstractmethod
    def create(self, entity: Question) -> Question: ...
