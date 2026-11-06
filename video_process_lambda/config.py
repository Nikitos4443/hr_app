import logging
import os
import time
from dataclasses import dataclass

import boto3
from faster_whisper import WhisperModel

MODEL_DIR = os.getenv("WHISPER_MODEL_DIR", "/opt/whisper-model")

model = WhisperModel(MODEL_DIR, device="cpu", compute_type="int8")

# Read from env first (local runs), the rest from SSM Parameter Store (SecureString).
# DATABASE_URL format for RDS Postgres: postgresql+psycopg://<user>:<password>@<host>:5432/<db>
PARAMETER_NAMES = ["DATABASE_URL"]
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@dataclass(frozen=True)
class Settings:
    database_url: str


def _load_parameters() -> dict:
    values = {name: os.environ[name] for name in PARAMETER_NAMES if os.getenv(name)}
    missing = [name for name in PARAMETER_NAMES if name not in values]
    if not missing:
        return values

    start = time.perf_counter()
    response = boto3.client("ssm").get_parameters(Names=missing, WithDecryption=True)
    if response["InvalidParameters"]:
        raise RuntimeError(f"Missing SSM parameters: {response['InvalidParameters']}")
    values.update({p["Name"]: p["Value"] for p in response["Parameters"]})
    logger.info("Loaded %s from SSM in %.3fs", missing, time.perf_counter() - start)
    return values


def _load_settings() -> Settings:
    values = _load_parameters()
    return Settings(database_url=values["DATABASE_URL"])


settings = _load_settings()
