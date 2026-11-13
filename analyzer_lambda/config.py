from dataclasses import dataclass

from dotenv import load_dotenv

from hr_core.config.parameters import load_parameters

load_dotenv()

PARAMETER_NAMES = ["DATABASE_URL", "GOOGLE_API_KEY"]

LLM_MODEL = "google_genai:gemini-3.5-flash-lite"


@dataclass(frozen=True)
class Settings:
    database_url: str
    google_api_key: str


def _load_settings() -> Settings:
    values = load_parameters(PARAMETER_NAMES)
    return Settings(
        database_url=values["DATABASE_URL"],
        google_api_key=values["GOOGLE_API_KEY"],
    )


settings = _load_settings()
