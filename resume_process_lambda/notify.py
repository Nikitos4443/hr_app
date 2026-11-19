from db import SessionLocal

from config import notification_channel, settings
from hr_core.models.vacancy_model import Vacancy
from hr_core.notifications.messages import send_invite, send_rejection
from hr_core.sql.repositories.SQLApplicationsRepository import SQLApplicationsRepository


def notify_invited(vacancy: Vacancy) -> list[int]:
    with SessionLocal() as session:
        applications = SQLApplicationsRepository(db=session)
        notified = []
        for application in applications.get_not_invited(vacancy.id):
            send_invite(notification_channel, application, vacancy, settings.frontend_url)
            applications.mark_screening_invited(application.id)
            notified.append(application.id)
        return notified


def notify_rejected(vacancy: Vacancy) -> list[int]:
    with SessionLocal() as session:
        applications = SQLApplicationsRepository(db=session)
        notified = []
        for application in applications.get_rejected_not_notified(vacancy.id):
            send_rejection(notification_channel, application, vacancy)
            applications.mark_rejection_notified(application.id)
            notified.append(application.id)
        return notified
