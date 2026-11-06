from beanie import Document, Indexed, init_beanie
from pydantic import BaseModel
from pymongo import AsyncMongoClient


class SalaryRange(BaseModel):
    min: int
    max: int
    currency: str


class Vacancy(Document):
    title: Indexed(str)
    company: Indexed(str)
    location: str
    employment_type: str
    experience_years_min: int
    description: str
    responsibilities: list[str]
    requirements: list[str]
    nice_to_have: list[str] = []
    salary_range: SalaryRange
    status: Indexed(str)

    class Settings:
        name = "vacancies"


class VacancyCandidate(Document):
    email: str
    vacancy_id: str

    class Settings:
        name = "candidates"


class CandidateVideoTranscriptions(Document):
    candidate_id: str
    transcription: str | None = None


async def init() -> AsyncMongoClient:
    client = AsyncMongoClient(
        "mongodb+srv://<db_username>:<db_password>@general.fifshpq.mongodb.net/"
    )

    await init_beanie(
        database=client.db_name,
        document_models=[Vacancy, VacancyCandidate, CandidateVideoTranscriptions],
    )
    return client
