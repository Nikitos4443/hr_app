from dataclasses import dataclass

from dotenv import load_dotenv
from hr_core.config.parameters import load_parameters
from hr_core.notifications.EmailNotificationChannel import EmailNotificationChannel
from hr_core.notifications.INotificationChannel import INotificationChannel

load_dotenv()

PARAMETER_NAMES = ["DATABASE_URL", "GOOGLE_API_KEY", "SMTP_USER", "SMTP_PASSWORD"]

SCORE_THRESHOLD = 50
MIN_CANDIDATES = 10
MAX_PAGES = 3


@dataclass(frozen=True)
class Settings:
    database_url: str
    google_api_key: str
    gmail_user: str
    gmail_app_password: str


def _load_settings() -> Settings:
    values = load_parameters(PARAMETER_NAMES)
    return Settings(
        database_url=values["DATABASE_URL"],
        google_api_key=values["GOOGLE_API_KEY"],
        gmail_user=values["SMTP_USER"],
        gmail_app_password=values["SMTP_PASSWORD"],
    )


settings = _load_settings()

notification_channel: INotificationChannel = EmailNotificationChannel(
    settings.gmail_user, settings.gmail_app_password
)
