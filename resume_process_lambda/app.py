
import json

import boto3
from process_cv import process_cv
import os
s3 = boto3.client("s3")

from urllib.parse import unquote_plus
def index(event, context):
    for record in event["Records"]:
        s3_event = json.loads(record['body'])
        for s3_record in s3_event.get("Records", []):
            bucket = s3_record['s3']['bucket']['name']
            key = unquote_plus(s3_record["s3"]["object"]["key"])
            _, vacancy_id, filename = key.split('/')
            local_path = f"/tmp/{filename}"
            s3.download_file(bucket, key, local_path)
            try:
                result = process_cv(local_path, vacancy_id)
            finally:
                os.remove(local_path)

    return {'result': result ,'statusCode': 200}

