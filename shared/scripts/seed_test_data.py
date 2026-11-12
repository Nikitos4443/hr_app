import os

from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.orm import Session

from hr_core.constants.index import BUCKET_VIDEOS_PREFIX
from hr_core.sql.session import create_session_factory
from hr_core.sql.tables import Applications, Questions, Users, Vacancies, VideoVerification

load_dotenv()

TEST_USERNAME = "test_hr"
# bcrypt hash of "test1234", so you can log in through the server as this user
TEST_PASSWORD_HASH = "$2b$12$rZIdS7Mgo6zmLyTl6y.PFOBfBEbAXgC3X37x9I5eOjlG1RyfTz3pq"

TEST_VACANCY_TITLE = "[TEST] Python Backend Developer"

QUESTIONS = [
    {"order": 1, "type": "video", "text": "Tell us about yourself.", "video_max_duration_sec": 120},
    {
        "order": 2,
        "type": "video",
        "text": "Describe the most challenging project you worked on.",
        "video_max_duration_sec": 180,
    },
    {"order": 3, "type": "text", "text": "Why do you want to join our company?"},
]

CANDIDATES = [
    {"email": "alice.test@example.com", "full_name": "Alice Test"},
    {"email": "bob.test@example.com", "full_name": "Bob Test"},
]


def get_or_create_user(session: Session) -> Users:
    user = session.scalar(select(Users).where(Users.username == TEST_USERNAME))
    if user is None:
        user = Users(username=TEST_USERNAME, password=TEST_PASSWORD_HASH, role="hr")
        session.add(user)
        session.flush()
    return user


def get_or_create_vacancy(session: Session, user: Users) -> Vacancies:
    vacancy = session.scalar(
        select(Vacancies).where(
            Vacancies.title == TEST_VACANCY_TITLE, Vacancies.created_by == user.id
        )
    )
    if vacancy is None:
        vacancy = Vacancies(
            title=TEST_VACANCY_TITLE,
            company="Test Company",
            location="Remote",
            employment_type="full-time",
            experience_years_min=2,
            description="Test vacancy created by seed_test_data.py",
            responsibilities=["Build REST APIs", "Maintain AWS lambdas"],
            requirements=["Python 3", "SQL", "AWS"],
            nice_to_have=["FastAPI", "Docker"],
            salary_min=2000,
            salary_max=4000,
            salary_currency="USD",
            status="open",
            created_by=user.id,
        )
        session.add(vacancy)
        session.flush()
    return vacancy


def get_or_create_questions(session: Session, vacancy: Vacancies) -> list[Questions]:
    existing = {
        q.order: q
        for q in session.scalars(select(Questions).where(Questions.vacancy_id == vacancy.id))
    }
    questions = []
    for data in QUESTIONS:
        question = existing.get(data["order"])
        if question is None:
            question = Questions(vacancy_id=vacancy.id, **data)
            session.add(question)
        questions.append(question)
    session.flush()
    return questions


def get_or_create_application(
    session: Session, vacancy: Vacancies, candidate: dict
) -> Applications:
    application = session.scalar(
        select(Applications).where(
            Applications.vacancy_id == vacancy.id, Applications.email == candidate["email"]
        )
    )
    if application is None:
        application = Applications(vacancy_id=vacancy.id, status="pending", **candidate)
        session.add(application)
        session.flush()
    return application


def get_or_create_video_verification(
    session: Session, application: Applications, question: Questions
) -> VideoVerification:
    verification = session.scalar(
        select(VideoVerification).where(
            VideoVerification.application_id == application.id,
            VideoVerification.question_id == question.id,
        )
    )
    if verification is None:
        verification = VideoVerification(
            application_id=application.id, question_id=question.id, status="pending"
        )
        session.add(verification)
        session.flush()
    return verification


def seed(session: Session) -> list[tuple[Applications, Questions, VideoVerification]]:
    user = get_or_create_user(session)
    vacancy = get_or_create_vacancy(session, user)
    questions = get_or_create_questions(session, vacancy)
    video_questions = [q for q in questions if q.type == "video"]

    rows = []
    for candidate in CANDIDATES:
        application = get_or_create_application(session, vacancy, candidate)
        for question in video_questions:
            verification = get_or_create_video_verification(session, application, question)
            rows.append((application, question, verification))
    return rows


def main() -> None:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is not set. "
            "Run e.g.: uv run --env-file ../server/.env python scripts/seed_test_data.py"
        )

    session_factory = create_session_factory(database_url)
    with session_factory() as session, session.begin():
        rows = seed(session)

        print("Seeded video_verification rows. Upload test videos to these S3 keys:")
        for application, question, verification in rows:
            print(
                f"  id={verification.id:<4} status={verification.status:<10} "
                f"{application.email:<26} q{question.order}  ->  "
                f"{BUCKET_VIDEOS_PREFIX}{verification.id}"
            )


if __name__ == "__main__":
    main()
