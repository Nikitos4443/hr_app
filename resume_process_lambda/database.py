import logging
import time

from bson import ObjectId
from dotenv import load_dotenv
from bson.errors import InvalidId
from pymongo import MongoClient

from config import settings

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

_client = None


def get_db():
    global _client
    if _client is None:
        start = time.perf_counter()
        print("Connecting to mongo")
        _client = MongoClient(settings.mongo_uri, serverSelectionTimeoutMS=5000)
        _client.admin.command("ping")
        logger.info("Mongo connected in %.3fs", time.perf_counter() - start)
    return _client[settings.mongo_db_name]


def get_vacancy(id: str):
    logger.info("get_vacancy called with id=%s", id)
    query = {"_id": ObjectId(id)}
    db = get_db()

    start = time.perf_counter()
    vacancy = db["vacancies"].find_one(query)
    logger.info(
        "find_one vacancies took %.3fs, found=%s",
        time.perf_counter() - start,
        vacancy is not None,
    )

    if vacancy is None:
        return None
    vacancy["_id"] = str(vacancy["_id"])
    return vacancy
