from datetime import datetime
from typing import Literal, Self

from pydantic import BaseModel, Field, field_validator, model_validator

from hr_core.models.vacancy_model import Vacancy


def _validate_title(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError("Назва вакансії не може бути порожньою")
    return value


def _validate_deadline(value: datetime | None) -> datetime | None:
    if value is not None and value.tzinfo is None:
        raise ValueError("deadline_at має містити часову зону, напр. 2026-12-01T18:00:00Z")
    return value


class _SalaryRangeMixin(BaseModel):
    salary_min: int | None = Field(default=None, ge=0)
    salary_max: int | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def check_salary_range(self) -> Self:
        if (
            self.salary_min is not None
            and self.salary_max is not None
            and self.salary_min > self.salary_max
        ):
            raise ValueError("salary_min не може бути більшим за salary_max")
        return self


class CreateVacancyDTO(_SalaryRangeMixin):
    title: str
    location: str | None = None
    employment_type: str | None = None
    experience_years_min: int | None = Field(default=None, ge=0)
    description: str | None = None
    responsibilities: list[str] = Field(default_factory=list)
    requirements: list[str] = Field(default_factory=list)
    nice_to_have: list[str] = Field(default_factory=list)
    salary_currency: str | None = None
    status: Literal["open", "closed"] = "open"
    deadline_at: datetime | None = None

    _check_title = field_validator("title")(_validate_title)
    _check_deadline = field_validator("deadline_at")(_validate_deadline)


class UpdateVacancyDTO(_SalaryRangeMixin):
    title: str | None = None
    location: str | None = None
    employment_type: str | None = None
    experience_years_min: int | None = Field(default=None, ge=0)
    description: str | None = None
    responsibilities: list[str] | None = None
    requirements: list[str] | None = None
    nice_to_have: list[str] | None = None
    salary_currency: str | None = None
    status: Literal["open", "closed"] | None = None
    deadline_at: datetime | None = None

    @field_validator("title")
    @classmethod
    def check_title(cls, value: str | None) -> str | None:
        return None if value is None else _validate_title(value)

    _check_deadline = field_validator("deadline_at")(_validate_deadline)


class VacancyResponse(Vacancy):
    applications_count: int = 0
    questions_count: int = 0


class PublicVacancyResponse(BaseModel):
    """Candidate-facing vacancy: no internal ids, authorship or selection state."""

    id: int
    title: str
    company: str
    company_description: str | None = None
    company_website: str | None = None
    location: str | None = None
    employment_type: str | None = None
    experience_years_min: int | None = None
    description: str | None = None
    responsibilities: list[str] = Field(default_factory=list)
    requirements: list[str] = Field(default_factory=list)
    nice_to_have: list[str] = Field(default_factory=list)
    salary_min: int | None = None
    salary_max: int | None = None
    salary_currency: str | None = None
    status: str
    deadline_at: datetime | None = None
