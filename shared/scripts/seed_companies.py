"""Seed a few companies and vacancies (idempotent).

Run from shared/:
    uv run --env-file ../.env python scripts/seed_companies.py
"""

import os
from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from hr_core.sql.session import create_session_factory
from hr_core.sql.tables import Companies, Users, Vacancies


HR_USERNAME = "test_hr"
# bcrypt hash of "test1234"
HR_PASSWORD_HASH = "$2b$12$rZIdS7Mgo6zmLyTl6y.PFOBfBEbAXgC3X37x9I5eOjlG1RyfTz3pq"

COMPANIES = [
    {
        "name": "Nimbus Cloud",
        "website": "https://nimbus-cloud.example.com",
        "description": (
            "Nimbus Cloud builds a managed Kubernetes platform for mid-size SaaS companies. "
            "Around 120 employees, fully remote across Europe, engineering-driven culture "
            "with quarterly hackathons and a yearly learning budget of $1500 per person."
        ),
    },
    {
        "name": "GreenLeaf Retail",
        "website": "https://greenleaf.example.com",
        "description": (
            "GreenLeaf Retail is a chain of 40 eco-friendly grocery stores in Ukraine and Poland "
            "with its own e-commerce app. About 900 employees; the tech team of 35 people "
            "works from the Lviv office in a hybrid format."
        ),
    },
    {
        "name": "Pixel Forge Studio",
        "website": "https://pixelforge.example.com",
        "description": (
            "Pixel Forge Studio is an independent game studio making mobile puzzle games "
            "with 10M+ downloads. A team of 45 people in Kyiv, flat structure, "
            "flexible hours and a 4-day work week in summer."
        ),
    },
]

VACANCIES = [
    {
        "company": "Nimbus Cloud",
        "title": "Senior DevOps Engineer",
        "location": "Remote (EU)",
        "employment_type": "full-time",
        "experience_years_min": 4,
        "description": "Own the reliability of our multi-tenant Kubernetes platform.",
        "responsibilities": [
            "Maintain and scale Kubernetes clusters on AWS",
            "Build CI/CD pipelines and infrastructure as code",
            "Participate in on-call rotation",
        ],
        "requirements": ["Kubernetes", "Terraform", "AWS", "Linux", "4+ years in DevOps/SRE"],
        "nice_to_have": ["Go", "Prometheus / Grafana", "CKA certification"],
        "salary_min": 4500,
        "salary_max": 6000,
        "salary_currency": "USD",
        "deadline_days": 30,
    },
    {
        "company": "GreenLeaf Retail",
        "title": "Middle Frontend Developer (React)",
        "location": "Lviv (hybrid)",
        "employment_type": "full-time",
        "experience_years_min": 2,
        "description": "Develop the customer-facing web shop and the internal admin panel.",
        "responsibilities": [
            "Build new features for the online store",
            "Work with designers on UI/UX improvements",
            "Write unit and e2e tests",
        ],
        "requirements": ["React", "TypeScript", "REST APIs", "2+ years of commercial experience"],
        "nice_to_have": ["Next.js", "Playwright", "Experience in e-commerce"],
        "salary_min": 2200,
        "salary_max": 3200,
        "salary_currency": "USD",
        "deadline_days": 21,
    },
    {
        "company": "Pixel Forge Studio",
        "title": "Junior QA Engineer",
        "location": "Kyiv (office)",
        "employment_type": "full-time",
        "experience_years_min": 0,
        "description": "Test our mobile puzzle games before every release.",
        "responsibilities": [
            "Manual testing of iOS and Android builds",
            "Write and maintain test cases",
            "Report and verify bugs in Jira",
        ],
        "requirements": ["Basic QA theory", "Attention to detail", "English B1+"],
        "nice_to_have": ["Love for mobile games", "Basic SQL"],
        "salary_min": None,
        "salary_max": None,
        "salary_currency": None,
        "deadline_days": None,
    },
]


def get_or_create_hr(session: Session) -> Users:
    user = session.scalar(select(Users).where(Users.username == HR_USERNAME))
    if user is None:
        user = Users(username=HR_USERNAME, password=HR_PASSWORD_HASH, role="hr")
        session.add(user)
        session.flush()
    return user


def seed_companies(session: Session) -> dict[str, Companies]:
    result = {}
    for data in COMPANIES:
        company = session.scalar(select(Companies).where(Companies.name == data["name"]))
        if company is None:
            company = Companies(**data)
            session.add(company)
            session.flush()
            print(f"+ company {company.id}: {company.name}")
        else:
            print(f"= company {company.id}: {company.name} (exists)")
        result[company.name] = company
    return result


def seed_vacancies(session: Session, companies: dict[str, Companies], hr: Users) -> None:
    now = datetime.now(UTC)
    for data in VACANCIES:
        data = dict(data)
        company = companies[data.pop("company")]
        deadline_days = data.pop("deadline_days")
        vacancy = session.scalar(
            select(Vacancies).where(
                Vacancies.title == data["title"], Vacancies.company_id == company.id
            )
        )
        if vacancy is not None:
            print(f"= vacancy {vacancy.id}: {vacancy.title} (exists)")
            continue
        vacancy = Vacancies(
            **data,
            company=company.name,
            company_id=company.id,
            status="open",
            created_by=hr.id,
            deadline_at=now + timedelta(days=deadline_days) if deadline_days else None,
        )
        session.add(vacancy)
        session.flush()
        print(f"+ vacancy {vacancy.id}: {vacancy.title} @ {company.name}")


def main() -> None:
    session_factory = create_session_factory(os.environ["DATABASE_URL"])
    with session_factory() as session:
        hr = get_or_create_hr(session)
        companies = seed_companies(session)
        seed_vacancies(session, companies, hr)
        session.commit()


if __name__ == "__main__":
    main()
