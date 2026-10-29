
import json

import boto3
from process_cv import process_cv
import os
s3 = boto3.client("s3")


from urllib.parse import unquote_plus
def index(event, context):
    print("Iterating records")
    for record in event["Records"]:
        print("Got record")
        s3_event = json.loads(record['body'])
        print("Loaded event")
        for s3_record in s3_event.get("Records", []):
            print("Getting bucket name")
            bucket = s3_record['s3']['bucket']['name']
            print("Gettin key")
            key = unquote_plus(s3_record["s3"]["object"]["key"])
            print("Parsing vacancy id")
            _, vacancy_id, filename = key.split('/')
            local_path = f"/tmp/{filename}"
            print("Downloading file")
            s3.download_file(bucket, key, local_path)
            try:
                print("Processing CV")
                result = process_cv(local_path, vacancy_id)
            finally:
                os.remove(local_path)

    return {'result': result ,'statusCode': 200}

