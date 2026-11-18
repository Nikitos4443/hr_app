import logging
from datetime import UTC, datetime

from fastapi import HTTPException
from modules.applications.dto.application_dto import (
    AnswerDetail,
    ApplicationActionResult,
    ApplicationCounts,
    ApplicationDetailResponse,
    ApplicationListItem,
    ApplicationListResponse,
    BulkActionResponse,
    BulkFailure,
    ResumeDetail,
    ResumeReview,
    TimelineEvent,
)
from modules.applications.IApplicationManagementService import IApplicationManagementService
from modules.auth.dto.principal import AuthPrincipal
from modules.vacancies.IVacancyService import IVacancyService
from starlette import status

from hr_core.models.application_model import Application
from hr_core.models.vacancy_model import Vacancy
from hr_core.notifications.INotificationChannel import INotificationChannel
from hr_core.notifications.messages import send_invite, send_rejection
from hr_core.repository_interfaces.IApplicationsRepository import (
    APPLICATION_STATUSES,
    IApplicationsRepository,
)
from hr_core.repository_interfaces.IEvaluationsRepository import IEvaluationsRepository
from hr_core.repository_interfaces.IQuestionsRepository import IQuestionsRepository
from hr_core.repository_interfaces.IResumeVerificationRepository import (
    IResumeVerificationRepository,
)
from hr_core.repository_interfaces.ITextVerificationRepository import (
    ITextVerificationRepository,
)
from hr_core.repository_interfaces.IVideoVerificationRepository import (
    IVideoVerificationRepository,
)
from hr_core.s3.service import S3Service
from hr_core.services.CandidateCleanupService import CandidateCleanupService

logger = logging.getLogger(__name__)


def _not_found() -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")


def _conflict(detail: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)


def _utc(value: datetime) -> datetime:
    # Some backends (SQLite) drop the timezone; stored timestamps are always UTC.
    return value.replace(tzinfo=UTC) if value.tzinfo is None else value


class ApplicationManagementService(IApplicationManagementService):
    def __init__(
        self,
        vacancies_service: IVacancyService,
        applications: IApplicationsRepository,
        resumes: IResumeVerificationRepository,
        questions: IQuestionsRepository,
        texts: ITextVerificationRepository,
        videos: IVideoVerificationRepository,
        evaluations: IEvaluationsRepository,
        cleanup: CandidateCleanupService,
        s3: S3Service,
        bucket_name: str,
        channel: INotificationChannel,
        frontend_url: str,
    ):
        self.vacancies_service = vacancies_service
        self.applications = applications
        self.resumes = resumes
        self.questions = questions
        self.texts = texts
        self.videos = videos
        self.evaluations = evaluations
        self.cleanup = cleanup
        self.s3 = s3
        self.bucket_name = bucket_name
        self.channel = channel
        self.frontend_url = frontend_url

    # ---- reads -------------------------------------------------------------------------

    def list_applications(
        self,
        actor: AuthPrincipal,
        vacancy_id: int,
        *,
        status: str | None,
        search: str | None,
        sort: str,
        descending: bool,
        limit: int,
        offset: int,
    ) -> ApplicationListResponse:
        self.vacancies_service.get_vacancy(actor, vacancy_id)
        summaries, total = self.applications.list_summaries(
            vacancy_id,
            status=status,
            search=(search or "").strip() or None,
            sort=sort,
            descending=descending,
            limit=limit,
            offset=offset,
        )
        total_questions = len(self.questions.list_by_vacancy(vacancy_id))
        by_status = self.applications.count_by_status(vacancy_id)
        counts = ApplicationCounts(
            all=sum(by_status.values()), **{s: by_status.get(s, 0) for s in APPLICATION_STATUSES}
        )
        return ApplicationListResponse(
            items=[ApplicationListItem.from_summary(s, total_questions) for s in summaries],
            total=total,
            counts=counts,
        )

    def get_application(
        self, actor: AuthPrincipal, application_id: int
    ) -> ApplicationDetailResponse:
        application, _ = self._load(actor, application_id)
        resume = self.resumes.get_by_application(application.id)
        evaluation = self.evaluations.get_by_application(application.id)
        answers, answer_times = self._answers(application)

        file_url = None
        if resume is not None and resume.status == "done" and application.purged_at is None:
            file_url = self.s3.create_presigned_get_url(
                self.bucket_name, self.s3.get_resume_key(application.id)
            )
        return ApplicationDetailResponse(
            id=application.id,
            vacancy_id=application.vacancy_id,
            email=application.email,
            full_name=application.full_name,
            status=application.derived_status(),
            created_at=application.created_at,
            resume=ResumeDetail(
                status=resume.status if resume else None,
                score=resume.score if resume else None,
                review=ResumeReview.model_validate(resume.llm_review)
                if resume and resume.llm_review
                else None,
                file_url=file_url,
            ),
            rank=evaluation.order if evaluation else None,
            ai_summary=evaluation.summary if evaluation else None,
            answers=answers,
            timeline=self._timeline(
                application, resume.processed_at if resume else None, answers, answer_times
            ),
        )

    # ---- actions -----------------------------------------------------------------------

    def invite(self, actor: AuthPrincipal, application_id: int) -> ApplicationActionResult:
        application, vacancy = self._load(actor, application_id)
        return self._invite(application, vacancy)

    def shortlist(self, actor: AuthPrincipal, application_id: int) -> ApplicationActionResult:
        application, _ = self._load(actor, application_id)
        return self._shortlist(application)

    def reject(self, actor: AuthPrincipal, application_id: int) -> ApplicationActionResult:
        application, vacancy = self._load(actor, application_id)
        return self._reject(application, vacancy)

    def bulk_action(
        self, actor: AuthPrincipal, vacancy_id: int, ids: list[int], action: str
    ) -> BulkActionResponse:
        vacancy = Vacancy.model_validate(self.vacancies_service.get_vacancy(actor, vacancy_id))
        updated: list[int] = []
        failed: list[BulkFailure] = []
        for application_id in dict.fromkeys(ids):
            try:
                application = self.applications.get_by_id(application_id)
                if application is None or application.vacancy_id != vacancy_id:
                    raise _not_found()
                if action == "invite":
                    self._invite(application, vacancy)
                elif action == "shortlist":
                    self._shortlist(application)
                else:
                    self._reject(application, vacancy)
                updated.append(application_id)
            except HTTPException as e:
                failed.append(BulkFailure(id=application_id, detail=str(e.detail)))
        return BulkActionResponse(updated=updated, failed=failed)

    def _invite(self, application: Application, vacancy: Vacancy) -> ApplicationActionResult:
        if application.status == "rejected":
            raise _conflict("Application was rejected")
        if application.status == "shortlisted":
            raise _conflict("Application is already shortlisted")
        if application.screening_invited_at is not None:
            return self._result(application)  # idempotent

        resume = self.resumes.get_by_application(application.id)
        if resume is None or resume.status != "done":
            raise _conflict("Resume is not processed yet")
        try:
            send_invite(self.channel, application, vacancy, self.frontend_url)
        except Exception as e:
            logger.exception("Failed to send screening invite for application %s", application.id)
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY, detail="Failed to send the invitation"
            ) from e
        self.applications.mark_screening_invited(application.id)
        return self._result(self._reload(application.id))

    def _shortlist(self, application: Application) -> ApplicationActionResult:
        if application.status == "rejected":
            raise _conflict("Application was rejected")
        if application.status == "shortlisted":
            return self._result(application)  # idempotent
        return self._result(self.applications.update_status(application.id, "shortlisted"))

    def _reject(self, application: Application, vacancy: Vacancy) -> ApplicationActionResult:
        if application.status == "rejected":
            return self._result(application)  # idempotent; leftovers are retried by the lambda
        rejected = self.applications.update_status(application.id, "rejected")

        # Same follow-up the resume lambda does for auto-rejected candidates. The decision is
        # already saved, so a failure here is logged and picked up by the lambda's next run
        # (rejection_notified_at / purged_at stay empty).
        try:
            send_rejection(self.channel, rejected, vacancy)
            self.applications.mark_rejection_notified(application.id)
        except Exception:
            logger.exception("Failed to send rejection for application %s", application.id)
        try:
            self.cleanup.purge(application.id)
        except Exception:
            logger.exception("Failed to purge data of application %s", application.id)
        return self._result(self._reload(application.id))

    # ---- helpers -----------------------------------------------------------------------

    def _load(self, actor: AuthPrincipal, application_id: int) -> tuple[Application, Vacancy]:
        application = self.applications.get_by_id(application_id)
        if application is None:
            raise _not_found()
        try:
            vacancy = self.vacancies_service.get_vacancy(actor, application.vacancy_id)
        except HTTPException as e:
            if e.status_code == status.HTTP_404_NOT_FOUND:
                raise _not_found() from e
            raise
        return application, Vacancy.model_validate(vacancy)

    def _reload(self, application_id: int) -> Application:
        return self.applications.get_by_id(application_id)

    @staticmethod
    def _result(application: Application) -> ApplicationActionResult:
        return ApplicationActionResult(
            id=application.id,
            status=application.derived_status(),
            screening_invited_at=application.screening_invited_at,
            status_changed_at=application.status_changed_at,
        )

    def _answers(self, application: Application) -> tuple[list[AnswerDetail], list[datetime]]:
        texts = {t.question_id: t for t in self.texts.list_by_application(application.id)}
        videos = {v.question_id: v for v in self.videos.list_by_application(application.id)}
        answers = []
        for question in self.questions.list_by_vacancy(application.vacancy_id):
            text = texts.get(question.id) if question.type == "text" else None
            video = videos.get(question.id) if question.type == "video" else None
            record = text or video
            answers.append(
                AnswerDetail(
                    question_id=question.id,
                    order=question.order,
                    type=question.type,
                    text=question.text,
                    status=record.status if record else "pending",
                    answer=text.answer if text else None,
                    transcription=video.transcription if video else None,
                )
            )
        records = [*texts.values(), *videos.values()]
        done_times = [r.processed_at for r in records if r.status == "done" and r.processed_at]
        return answers, done_times

    def _timeline(
        self,
        application: Application,
        resume_processed_at: datetime | None,
        answers: list[AnswerDetail],
        answer_times: list[datetime],
    ) -> list[TimelineEvent]:
        events: list[tuple[str, datetime | None]] = [
            ("applied", application.created_at),
            ("resume_processed", resume_processed_at),
            ("screening_invited", application.screening_invited_at),
            ("rejection_notified", application.rejection_notified_at),
        ]
        if application.status in ("shortlisted", "rejected"):
            events.append((application.status, application.status_changed_at))
        if answers and all(a.status == "done" for a in answers):
            completed_at = max((_utc(t) for t in answer_times), default=None)
            events.append(("screening_completed", completed_at))
        return sorted(
            (TimelineEvent(type=kind, at=_utc(at)) for kind, at in events if at is not None),
            key=lambda event: event.at,
        )
