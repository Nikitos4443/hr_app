import logging
import tempfile

from event_parser import parse_event_download_s3_file
from save_to_db import save_to_db
from transcribe_video import transcribe

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def index(event, context):
    with tempfile.TemporaryDirectory() as local_dir:
        parsed = parse_event_download_s3_file(event, local_dir)
        if parsed is None:
            logger.info("No S3 records in event: %s", event)
            return {"statusCode": 200}

        file_path, file_id = parsed
        # S3 key is raw/videos/<video_verification.id>.<ext>
        verification_id = int(file_id)
        text = transcribe(file_path)
        save_to_db(verification_id, text)

    logger.info("Saved transcription for video_verification %s", verification_id)
    return {"statusCode": 200}
