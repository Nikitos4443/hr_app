from hr_core.models.application_model import Application
from hr_core.models.vacancy_model import Vacancy
from hr_core.notifications.INotificationChannel import INotificationChannel

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


def send_message(
    channel: INotificationChannel,
    application: Application,
    vacancy: Vacancy,
    subject: str,
    body: str,
    **extra,
) -> None:
    name = f" {application.full_name}" if application.full_name else ""
    channel.send(
        recipient=application.email,
        subject=subject.format(title=vacancy.title, company=vacancy.company),
        body=body.format(name=name, title=vacancy.title, company=vacancy.company, **extra),
    )


def send_invite(
    channel: INotificationChannel, application: Application, vacancy: Vacancy, frontend_url: str
) -> None:
    link = f"{frontend_url}/screening/{application.screening_token}"
    send_message(channel, application, vacancy, INVITE_SUBJECT, INVITE_BODY, link=link)


def send_rejection(
    channel: INotificationChannel, application: Application, vacancy: Vacancy
) -> None:
    send_message(channel, application, vacancy, REJECT_SUBJECT, REJECT_BODY)
