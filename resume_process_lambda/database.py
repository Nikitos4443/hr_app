import logging
import os
import time

from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

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
        _client = MongoClient(os.environ["MONGO_URI"], serverSelectionTimeoutMS=5000)
        _client.admin.command("ping")
        logger.info("Mongo connected in %.3fs", time.perf_counter() - start)
    db_name = os.getenv("MONGO_DB_NAME")
    return _client[db_name] if db_name else _client.get_default_database()


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
