from config import notification_channel
from db import SessionLocal

from hr_core.models.vacancy_model import Vacancy
from hr_core.sql.repositories.SQLApplicationsRepository import SQLApplicationsRepository

SUBJECT = "Your application for {title} at {company}"

BODY = """Hello{name},

Thank you for your interest in the {title} position at {company} and for the time you spent applying.

After reviewing all applications, we have decided to move forward with other candidates whose experience more closely matches the requirements of this role.

We wish you the best of luck in your job search.

Best regards,
{company} recruiting team"""  # noqa: E501


def notify_rejected(vacancy: Vacancy) -> list[int]:
    with SessionLocal() as session:
        applications = SQLApplicationsRepository(db=session)
        notified = []
        for application in applications.get_rejected_not_notified(vacancy.id):
            name = f" {application.full_name}" if application.full_name else ""
            notification_channel.send(
                recipient=application.email,
                subject=SUBJECT.format(title=vacancy.title, company=vacancy.company),
                body=BODY.format(name=name, title=vacancy.title, company=vacancy.company),
            )
            applications.mark_rejection_notified(application.id)
            notified.append(application.id)
        return notified
