import logging

import boto3
from botocore.exceptions import ClientError

from hr_core.constants.index import BUCKET_RESUME_PREFIX

s3_client = boto3.client("s3")


class S3Service:
    def create_presigned_post_url(self, bucket_name, object_name, expiration=3600):
        try:
            response = s3_client.generate_presigned_post(
                bucket_name, object_name, ExpiresIn=expiration
            )
        except ClientError as e:
            logging.error(e)
            return None

        return response

    def get_resume_key(self, application_id):
        return f"{BUCKET_RESUME_PREFIX}{application_id}.pdf"

    def delete_objects(self, bucket_name: str, keys: list[str]) -> None:
        if not keys:
            return
        response = s3_client.delete_objects(
            Bucket=bucket_name,
            Delete={"Objects": [{"Key": key} for key in keys], "Quiet": True},
        )
        if response.get("Errors"):
            raise RuntimeError(f"Failed to delete S3 objects: {response['Errors']}")
