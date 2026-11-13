from pydantic import BaseModel

from hr_core.models.question_model import Question
from hr_core.models.resume_verification_model import ResumeVerification
from hr_core.models.text_verification_model import TextVerification
from hr_core.models.video_verification_model import VideoVerification


class Answer(BaseModel):
    question_order: int
    question_type: str
    question: str
    answer: str


class Candidate(BaseModel):
    application_id: int
    resume_score: float
    resume_review: str
    answers: list[Answer]


def build_candidates(
    questions: list[Question],
    resumes: list[ResumeVerification],
    videos: list[VideoVerification],
    texts: list[TextVerification],
) -> list[Candidate]:
    video_answers = {
        (v.application_id, v.question_id): v.transcription
        for v in videos
        if v.transcription is not None
    }
    text_answers = {
        (t.application_id, t.question_id): t.answer for t in texts if t.answer is not None
    }

    candidates = []
    for resume in sorted(resumes, key=lambda r: r.application_id):
        if resume.score is None:
            continue

        answers = []
        for question in sorted(questions, key=lambda q: q.order):
            source = video_answers if question.type == "video" else text_answers
            answer = source.get((resume.application_id, question.id))
            if answer is None:
                break
            answers.append(
                Answer(
                    question_order=question.order,
                    question_type=question.type,
                    question=question.text,
                    answer=answer,
                )
            )
        else:
            candidates.append(
                Candidate(
                    application_id=resume.application_id,
                    resume_score=resume.score,
                    resume_review=(resume.llm_review or {}).get("description", ""),
                    answers=answers,
                )
            )
    return candidates
