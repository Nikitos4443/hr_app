import logging
import os
from dataclasses import dataclass

from faster_whisper import WhisperModel

from hr_core.config.parameters import load_parameters

MODEL_DIR = os.getenv("WHISPER_MODEL_DIR", "/opt/whisper-model")

model = WhisperModel(MODEL_DIR, device="cpu", compute_type="int8")

PARAMETER_NAMES = ["DATABASE_URL", "BUCKET_NAME"]
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@dataclass(frozen=True)
class Settings:
    database_url: str
    bucket_name: str


def _load_settings() -> Settings:
    values = load_parameters(PARAMETER_NAMES)
    return Settings(database_url=values["DATABASE_URL"], bucket_name=values["BUCKET_NAME"])


settings = _load_settings()
