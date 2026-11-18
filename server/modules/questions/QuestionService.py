from fastapi import HTTPException
from starlette import status

from hr_core.models.question_model import Question
from hr_core.repository_interfaces.IQuestionsRepository import IQuestionsRepository
from modules.auth.dto.principal import AuthPrincipal
from modules.questions.dto.question_dto import QuestionInputDTO
from modules.questions.IQuestionService import IQuestionService
from modules.vacancies.IVacancyService import IVacancyService


class QuestionService(IQuestionService):
    def __init__(self, repo: IQuestionsRepository, vacancies_service: IVacancyService):
        self.repo = repo
        self.vacancies_service = vacancies_service

    def list_questions(self, actor: AuthPrincipal, vacancy_id: int) -> list[Question]:
        self.vacancies_service.get_vacancy(actor, vacancy_id)  # ownership check, 404 otherwise
        return self.repo.list_by_vacancy(vacancy_id)

    def replace_questions(
        self, actor: AuthPrincipal, vacancy_id: int, items: list[QuestionInputDTO]
    ) -> list[Question]:
        self.vacancies_service.get_vacancy(actor, vacancy_id)
        if self.repo.has_answers(vacancy_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Questions cannot be changed because candidates have already answered",
            )
        return self.repo.replace_for_vacancy(
            vacancy_id,
            [
                Question(vacancy_id=vacancy_id, order=position, **item.model_dump())
                for position, item in enumerate(items, start=1)
            ],
        )
