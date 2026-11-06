import os
import time
import logging
from dataclasses import dataclass

import boto3
from faster_whisper import WhisperModel

MODEL_DIR = os.getenv("WHISPER_MODEL_DIR", "/opt/whisper-model")

model = WhisperModel(MODEL_DIR, device="cpu", compute_type="int8")

PARAMETER_NAMES = ["MONGO_URI", "MONGO_DB_NAME"]
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@dataclass(frozen=True)
class Settings:
    mongo_uri: str
    mongo_db_name: str
    google_api_key: str

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
    return Settings(
        mongo_uri=values["MONGO_URI"],
        mongo_db_name=values["MONGO_DB_NAME"],
        google_api_key=values["GOOGLE_API_KEY"],
    )


settings = _load_settings()