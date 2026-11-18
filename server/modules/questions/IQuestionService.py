from abc import ABC, abstractmethod

from hr_core.models.question_model import Question
from modules.auth.dto.principal import AuthPrincipal
from modules.questions.dto.question_dto import QuestionInputDTO


class IQuestionService(ABC):
    @abstractmethod
    def list_questions(self, actor: AuthPrincipal, vacancy_id: int) -> list[Question]: ...

    @abstractmethod
    def replace_questions(
        self, actor: AuthPrincipal, vacancy_id: int, items: list[QuestionInputDTO]
    ) -> list[Question]: ...
