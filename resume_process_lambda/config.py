import logging
import os
import time
from dataclasses import dataclass

import boto3
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

PARAMETER_NAMES = ["MONGO_URI", "MONGO_DB_NAME", "GOOGLE_API_KEY"]


@dataclass(frozen=True)
class Settings:
    mongo_uri: str
    mongo_db_name: str
    google_api_key: str


def _load_parameters() -> dict:
    # Locally values come from .env, in Lambda everything missing is fetched from Parameter Store
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


# Runs once per cold start, warm invocations reuse the same object
settings = _load_settings()
