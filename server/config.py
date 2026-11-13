import os

from dotenv import load_dotenv

load_dotenv()


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Required environment variable {name} is not set")
    return value


SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", "sqlite:///./hrapp.db")
SECRET_KEY = _require_env("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "20"))
DATABASE_PROVIDER = os.getenv("DATABASE_PROVIDER", "sql")
MONGO_URI = os.getenv("MONGO_URI", "sql")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "sql")
BUCKET_NAME = _require_env("BUCKET_NAME")

LLM_MODEL = os.getenv("LLM")


from dataclasses import dataclass

from dotenv import load_dotenv
from hr_core.config.parameters import load_parameters
from hr_core.notifications.EmailNotificationChannel import EmailNotificationChannel
from hr_core.notifications.INotificationChannel import INotificationChannel

load_dotenv()

PARAMETER_NAMES = [
    "DATABASE_URL",
    "GOOGLE_API_KEY",
    "SMTP_USER",
    "SMTP_PASSWORD",
    "BUCKET_NAME",
    "FRONTEND_URL",
    "LLM_MODEL"
]

SCORE_THRESHOLD = 50
MIN_CANDIDATES = 10
MAX_PAGES = 3


@dataclass(frozen=True)
class Settings:
    database_url: str
    google_api_key: str
    gmail_user: str
    gmail_app_password: str
    bucket_name: str
    frontend_url: str
    llm_model: str


def _load_settings() -> Settings:
    values = load_parameters(PARAMETER_NAMES)
    return Settings(
        database_url=values["DATABASE_URL"],
        google_api_key=values["GOOGLE_API_KEY"],
        gmail_user=values["SMTP_USER"],
        gmail_app_password=values["SMTP_PASSWORD"],
        bucket_name=values["BUCKET_NAME"],
        frontend_url=values["FRONTEND_URL"].rstrip("/"),
        llm_model=values["LLM_MODEL"]
    )


settings = _load_settings()