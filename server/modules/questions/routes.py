from typing import Annotated

from fastapi import APIRouter, Body, Depends
from fastapi_utils.cbv import cbv
from ioc.index import get_question_service

from hr_core.models.question_model import Question
from hr_core.models.user_model import UserRole
from modules.auth.guards import CurrentPrincipalDep, require_roles
from modules.questions.dto.question_dto import MAX_QUESTIONS, QuestionInputDTO
from modules.questions.IQuestionService import IQuestionService

router = APIRouter(prefix="/vacancies", tags=["questions"])


@cbv(router)
class QuestionsRouter:
    question_service: IQuestionService = Depends(get_question_service)

    @router.get("/{vacancy_id}/questions", response_model=list[Question])
    @require_roles(UserRole.COMPANY_ADMIN, UserRole.HR)
    async def list_questions(self, vacancy_id: int, principal: CurrentPrincipalDep):
        return self.question_service.list_questions(principal, vacancy_id)

    @router.put("/{vacancy_id}/questions", response_model=list[Question])
    @require_roles(UserRole.COMPANY_ADMIN, UserRole.HR)
    async def replace_questions(
        self,
        vacancy_id: int,
        items: Annotated[list[QuestionInputDTO], Body(max_length=MAX_QUESTIONS)],
        principal: CurrentPrincipalDep,
    ):
        return self.question_service.replace_questions(principal, vacancy_id, items)
