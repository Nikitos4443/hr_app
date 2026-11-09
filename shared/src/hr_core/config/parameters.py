import logging
import os
import time
from collections.abc import Sequence

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def load_parameters(names: Sequence[str]) -> dict[str, str]:
    values = {name: os.environ[name] for name in names if os.getenv(name)}
    missing = [name for name in names if name not in values]
    if not missing:
        return values

    import boto3

    start = time.perf_counter()
    response = boto3.client("ssm").get_parameters(Names=missing, WithDecryption=True)
    if response["InvalidParameters"]:
        raise RuntimeError(f"Missing SSM parameters: {response['InvalidParameters']}")
    values.update({p["Name"]: p["Value"] for p in response["Parameters"]})
    logger.info("Loaded %s from SSM in %.3fs", missing, time.perf_counter() - start)
    return values
