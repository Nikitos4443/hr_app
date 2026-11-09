from db import SessionLocal

from config import notification_channel, settings
from hr_core.models.application_model import Application
from hr_core.models.vacancy_model import Vacancy
from hr_core.sql.repositories.SQLApplicationsRepository import SQLApplicationsRepository

INVITE_SUBJECT = "Next step for {title} at {company}: screening"

INVITE_BODY = """Hello{name},

Thank you for applying to the {title} position at {company}. We have reviewed your resume and would like to invite you to the next step: a short screening where you answer a few questions.

Start the screening here:
{link}

Best regards,
{company} recruiting team"""  # noqa: E501

REJECT_SUBJECT = "Your application for {title} at {company}"

REJECT_BODY = """Hello{name},

Thank you for your interest in the {title} position at {company} and for the time you spent applying.

After reviewing all applications, we have decided to move forward with other candidates whose experience more closely matches the requirements of this role.

We wish you the best of luck in your job search.

Best regards,
{company} recruiting team"""  # noqa: E501


def notify_invited(vacancy: Vacancy) -> list[int]:
    with SessionLocal() as session:
        applications = SQLApplicationsRepository(db=session)
        notified = []
        for application in applications.get_not_invited(vacancy.id):
            link = f"{settings.frontend_url}/screening/{application.screening_token}"
            _send(application, vacancy, INVITE_SUBJECT, INVITE_BODY, link=link)
            applications.mark_screening_invited(application.id)
            notified.append(application.id)
        return notified


def notify_rejected(vacancy: Vacancy) -> list[int]:
    with SessionLocal() as session:
        applications = SQLApplicationsRepository(db=session)
        notified = []
        for application in applications.get_rejected_not_notified(vacancy.id):
            _send(application, vacancy, REJECT_SUBJECT, REJECT_BODY)
            applications.mark_rejection_notified(application.id)
            notified.append(application.id)
        return notified


def _send(application: Application, vacancy: Vacancy, subject: str, body: str, **extra) -> None:
    name = f" {application.full_name}" if application.full_name else ""
    notification_channel.send(
        recipient=application.email,
        subject=subject.format(title=vacancy.title, company=vacancy.company),
        body=body.format(name=name, title=vacancy.title, company=vacancy.company, **extra),
    )
