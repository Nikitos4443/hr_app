from hr_core.models.application_model import Application
from hr_core.models.question_model import Question
from hr_core.repository_interfaces.IQuestionsRepository import IQuestionsRepository
from hr_core.repository_interfaces.IResumeVerificationRepository import (
    IResumeVerificationRepository,
)
from modules.flow.errors import ScreeningError


def ensure_screening_available(
    application: Application, resumes: IResumeVerificationRepository
) -> None:
    if application.purged_at is not None:
        raise ScreeningError(410, "Application data was removed")
    if application.status == "rejected":
        raise ScreeningError(403, "Application was rejected")
    if application.screening_invited_at is None:
        raise ScreeningError(403, "Screening is not available yet")

    resume = resumes.get_by_application(application.id)
    if resume is None or resume.status != "done":
        raise ScreeningError(409, "Resume is not processed yet")


def get_answerable_question(
    application: Application,
    question_id: int,
    question_type: str,
    questions: IQuestionsRepository,
    resumes: IResumeVerificationRepository,
) -> Question:
    ensure_screening_available(application, resumes)

    question = questions.get_by_id(question_id)
    if (
        question is None
        or question.vacancy_id != application.vacancy_id
        or question.type != question_type
    ):
        raise ScreeningError(404, f"{question_type.capitalize()} question not found")
    return question
