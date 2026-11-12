from hr_core.models.application_model import Application
from hr_core.models.text_verification_model import TextVerification
from hr_core.repository_interfaces.IQuestionsRepository import IQuestionsRepository
from hr_core.repository_interfaces.IResumeVerificationRepository import (
    IResumeVerificationRepository,
)
from hr_core.repository_interfaces.ITextVerificationRepository import (
    ITextVerificationRepository,
)
from modules.flow.guards import get_answerable_question
from modules.flow.services.ITextService import ITextService


class TextService(ITextService):
    def __init__(
        self,
        texts: ITextVerificationRepository,
        questions: IQuestionsRepository,
        resumes: IResumeVerificationRepository,
    ):
        self.texts = texts
        self.questions = questions
        self.resumes = resumes

    async def save_answer(
        self, application: Application, question_id: int, answer: str
    ) -> TextVerification:
        get_answerable_question(application, question_id, "text", self.questions, self.resumes)
        return self.texts.save_answer(application.id, question_id, answer)
