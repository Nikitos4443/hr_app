from fastapi import HTTPException

from hr_core.models.application_model import Application
from hr_core.repository_interfaces.IQuestionsRepository import IQuestionsRepository
from hr_core.repository_interfaces.IResumeVerificationRepository import (
    IResumeVerificationRepository,
)
from hr_core.repository_interfaces.ITextVerificationRepository import (
    ITextVerificationRepository,
)
from hr_core.repository_interfaces.IVacanciesRepository import IVacanciesRepository
from hr_core.repository_interfaces.IVideoVerificationRepository import (
    IVideoVerificationRepository,
)
from modules.flow.dto.screening_dto import ScreeningQuestion, ScreeningResponse
from modules.flow.errors import ScreeningError
from modules.flow.guards import ensure_screening_available


class ScreeningService:
    def __init__(
        self,
        vacancies: IVacanciesRepository,
        questions: IQuestionsRepository,
        resumes: IResumeVerificationRepository,
        texts: ITextVerificationRepository,
        videos: IVideoVerificationRepository,
    ):
        self.vacancies = vacancies
        self.questions = questions
        self.resumes = resumes
        self.texts = texts
        self.videos = videos

    def get_view(self, application: Application) -> ScreeningResponse:
        try:
            ensure_screening_available(application, self.resumes)
        except ScreeningError as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail) from e

        print("AFTER")

        vacancy = self.vacancies.get_by_id(application.vacancy_id)
        answered_ids = {
            v.question_id
            for v in self.videos.list_by_application(application.id)
            if v.status == "done"
        } | {
            t.question_id
            for t in self.texts.list_by_application(application.id)
            if t.status == "done"
        }
        questions = [
            ScreeningQuestion(
                id=q.id,
                order=q.order,
                type=q.type,
                text=q.text,
                video_max_duration_sec=q.video_max_duration_sec,
                answered=q.id in answered_ids,
            )
            for q in self.questions.list_by_vacancy(application.vacancy_id)
        ]
        completed = bool(questions) and all(q.answered for q in questions)
        return ScreeningResponse(
            vacancy_title=vacancy.title,
            company_name=vacancy.company,
            status=application.status,
            screening_progress="completed" if completed else "in_progress",
            questions=questions,
        )
