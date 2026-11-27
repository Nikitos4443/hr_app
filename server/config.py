import os
from dataclasses import dataclass

from dotenv import load_dotenv
from guard import SecurityConfig
from guard_core.handlers.suspatterns_handler import ALL_DETECTION_CATEGORIES

from hr_core.config.parameters import load_parameters

load_dotenv()


ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "20"))
DATABASE_PROVIDER = os.getenv("DATABASE_PROVIDER", "sql")
MONGO_URI = os.getenv("MONGO_URI", "sql")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "sql")

PARAMETER_NAMES = [
    "SECRET_KEY",
    "DATABASE_URL",
    "GOOGLE_API_KEY",
    "SMTP_USER",
    "SMTP_PASSWORD",
    "BUCKET_NAME",
    "FRONTEND_URL",
    "LLM_MODEL",
    "ANALYZER_LAMBDA_ARN",
    "ANALYZER_SCHEDULER_ROLE_ARN",
]

SCORE_THRESHOLD = 50
MIN_CANDIDATES = 10
MAX_PAGES = 3


@dataclass(frozen=True)
class Settings:
    secret_key: str
    database_url: str
    google_api_key: str
    gmail_user: str
    gmail_app_password: str
    bucket_name: str
    frontend_url: str
    llm_model: str
    analyzer_lambda_arn: str
    analyzer_scheduler_role_arn: str


def _load_settings() -> Settings:
    values = load_parameters(PARAMETER_NAMES)
    return Settings(
        secret_key=values["SECRET_KEY"],
        database_url=values["DATABASE_URL"],
        google_api_key=values["GOOGLE_API_KEY"],
        gmail_user=values["SMTP_USER"],
        gmail_app_password=values["SMTP_PASSWORD"],
        bucket_name=values["BUCKET_NAME"],
        frontend_url=values["FRONTEND_URL"].rstrip("/"),
        llm_model=values["LLM_MODEL"],
        analyzer_lambda_arn=values["ANALYZER_LAMBDA_ARN"],
        analyzer_scheduler_role_arn=values["ANALYZER_SCHEDULER_ROLE_ARN"],
    )


settings = _load_settings()
SECRET_KEY = settings.secret_key
BUCKET_NAME = settings.bucket_name


security_config = SecurityConfig(
    enable_redis=False,
    enable_rate_limiting=True,
    rate_limit=100,
    rate_limit_window=60,
    enable_cors=True,
    cors_allow_origins=[settings.frontend_url],
    cors_allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    cors_allow_headers=["*"],
    cors_allow_credentials=True,
    cors_expose_headers=["X-Custom-Header"],
    cors_max_age=600,
    # The server never fetches user-supplied URLs, so SSRF scanning only
    # produces false positives (e.g. Referer: http://localhost:5173/...).
    enabled_detection_categories=ALL_DETECTION_CATEGORIES - {"ssrf"},
)
