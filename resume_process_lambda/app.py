import logging
import tempfile

from event_parser import parse_event_download_s3_files
from get_vacancy import get_vacancy
from notify import notify_invited, notify_rejected
from purge_rejected import purge_rejected
from save_to_db import save_to_db

from config import settings
from hr_core.s3.service import S3Service
from process_cv import process_cv

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def index(event, context):
    with tempfile.TemporaryDirectory() as local_dir:
        for file_path, s3_key, file_id in parse_event_download_s3_files(event, local_dir):
            application_id = int(file_id)
            vacancy = get_vacancy(application_id)
            result = process_cv(file_path, vacancy)
            if not result.is_resume:
                logger.info(
                    "Application %s file is not a resume: %s", application_id, result.description
                )
                S3Service().delete_objects(settings.bucket_name, [s3_key])
                continue

            rejected_id = save_to_db(application_id, vacancy.id, result)
            logger.info(
                "Saved resume score %s for application %s, rejected %s",
                result.score,
                application_id,
                rejected_id,
            )

            purged = purge_rejected(vacancy.id)
            logger.info("Purged applications %s", purged)

            notified_rejected = notify_rejected(vacancy)
            logger.info("Sent rejection to applications %s", notified_rejected)

            notified_invited = notify_invited(vacancy)
            logger.info("Sent screening invite to applications %s", notified_invited)

    return {"statusCode": 200}
