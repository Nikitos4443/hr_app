from hr_core.models.company_model import Company
from hr_core.models.vacancy_model import Vacancy

def _format_salary(v: Vacancy) -> str | None:
    if v.salary_min is None and v.salary_max is None:
        return None
    currency = v.salary_currency or ""
    if v.salary_min is not None and v.salary_max is not None:
        return f"{v.salary_min}-{v.salary_max} {currency}".strip()
    if v.salary_min is not None:
        return f"from {v.salary_min} {currency}".strip()
    return f"up to {v.salary_max} {currency}".strip()


def _bullets(items: list[str]) -> str:
    return "\n".join(f"  - {item}" for item in items)


def format_vacancy(v: Vacancy | None) -> str:
    if v is None:
        return "No vacancy information available."
    lines = [f"Title: {v.title}", f"Company: {v.company}"]
    if v.location:
        lines.append(f"Location: {v.location}")
    if v.employment_type:
        lines.append(f"Employment type: {v.employment_type}")
    if v.experience_years_min is not None:
        lines.append(f"Minimum experience: {v.experience_years_min} years")
    if salary := _format_salary(v):
        lines.append(f"Salary: {salary}")
    if v.deadline_at:
        lines.append(f"Application deadline: {v.deadline_at:%Y-%m-%d}")
    lines.append(f"Status: {v.status}")
    if v.description:
        lines.append(f"Description:\n{v.description}")
    if v.responsibilities:
        lines.append(f"Responsibilities:\n{_bullets(v.responsibilities)}")
    if v.requirements:
        lines.append(f"Requirements:\n{_bullets(v.requirements)}")
    if v.nice_to_have:
        lines.append(f"Nice to have:\n{_bullets(v.nice_to_have)}")
    return "\n".join(lines)


def format_company(c: Company | None, v: Vacancy | None = None) -> str:
    if c is None:
        if v is not None:
            return f"Name: {v.company}\nNo other company information available."
        return "No company information available."

    lines = [f"Name: {c.name}"]
    if c.website:
        lines.append(f"Website: {c.website}")
    if c.description:
        lines.append(f"Description:\n{c.description}")
    return "\n".join(lines)
