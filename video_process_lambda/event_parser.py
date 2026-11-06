import json
import os
from urllib.parse import unquote_plus

import boto3

s3 = boto3.client("s3")


def parse_event_download_s3_file(lambda_event, local_dir):
    for record in lambda_event["Records"]:
        s3_event = json.loads(record["body"])

        for s3_record in s3_event.get("Records", []):
            bucket = s3_record["s3"]["bucket"]["name"]
            key = unquote_plus(s3_record["s3"]["object"]["key"])
            # Key is raw/videos/<file_id>[.ext], the file name is the transcription document id
            file_name = key.rsplit("/", 1)[-1]
            file_id = os.path.splitext(file_name)[0]
            file_path = os.path.join(local_dir, file_name)

            s3.download_file(bucket, key, file_path)
            return file_path, file_id

    return None
