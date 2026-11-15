import os
from dataclasses import dataclass

from dotenv import load_dotenv
from guard import SecurityConfig

from hr_core.config.parameters import load_parameters

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


PARAMETER_NAMES = [
    "DATABASE_URL",
    "GOOGLE_API_KEY",
    "SMTP_USER",
    "SMTP_PASSWORD",
    "BUCKET_NAME",
    "FRONTEND_URL",
    "LLM_MODEL",
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
        llm_model=values["LLM_MODEL"],
    )


settings = _load_settings()


security_config = SecurityConfig(
    enable_redis=False,
    enable_rate_limiting=True,
    rate_limit=100,
    rate_limit_window=60,
    enable_cors=True,
    cors_allow_origins=[settings.frontend_url],
    cors_allow_methods=["GET", "POST"],
    cors_allow_headers=["*"],
    cors_allow_credentials=True,
    cors_expose_headers=["X-Custom-Header"],
    cors_max_age=600,
)
