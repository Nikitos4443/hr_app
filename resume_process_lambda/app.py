import logging
import tempfile

from event_parser import parse_event_download_s3_files
from get_vacancy import get_vacancy
from notify_rejected import notify_rejected
from process_cv import process_cv
from save_to_db import save_to_db

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def index(event, context):
    with tempfile.TemporaryDirectory() as local_dir:
        for file_path, s3_key, file_id in parse_event_download_s3_files(event, local_dir):
            application_id = int(file_id)
            vacancy = get_vacancy(application_id)
            result = process_cv(file_path, vacancy)
            if not result.is_resume:
                logger.info("Application %s file is not a resume: %s", application_id, result.description)
                continue

            rejected = save_to_db(application_id, vacancy.id, s3_key, result)
            logger.info("Saved resume score %s for application %s", result.score, application_id)
            if rejected is not None:
                logger.info("Rejected application %s", rejected.id)

            notified = notify_rejected(vacancy)
            if notified:
                logger.info("Notified rejected applications %s", notified)

    return {"statusCode": 200}
