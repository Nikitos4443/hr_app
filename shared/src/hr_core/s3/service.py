import logging

import boto3
from botocore.exceptions import ClientError

from hr_core.constants.index import (
    BUCKET_RESUME_PREFIX,
    BUCKET_VIDEOS_PREFIX,
    MAX_RESUME_SIZE_BYTES,
    MAX_VIDEO_SIZE_BYTES,
    RESUME_CONTENT_TYPE,
    VIDEO_CONTENT_TYPE_PREFIX,
)

s3_client = boto3.client("s3")


class S3Service:
    def create_presigned_post_url(
        self,
        bucket_name,
        object_name,
        expiration=3600,
        max_size_bytes=MAX_RESUME_SIZE_BYTES,
        content_type=RESUME_CONTENT_TYPE,
    ):
        try:
            response = s3_client.generate_presigned_post(
                bucket_name,
                object_name,
                Fields={"Content-Type": content_type},
                Conditions=[
                    ["content-length-range", 1, max_size_bytes],
                    ["eq", "$Content-Type", content_type],
                ],
                ExpiresIn=expiration,
            )
        except ClientError as e:
            logging.error(e)
            return None

        return response

    def create_video_presigned_post_url(self, bucket_name, object_name, expiration=3600):
        try:
            return s3_client.generate_presigned_post(
                bucket_name,
                object_name,
                Conditions=[
                    ["content-length-range", 1, MAX_VIDEO_SIZE_BYTES],
                    ["starts-with", "$Content-Type", VIDEO_CONTENT_TYPE_PREFIX],
                ],
                ExpiresIn=expiration,
            )
        except ClientError as e:
            logging.error(e)
            return None

    def get_resume_key(self, application_id):
        return f"{BUCKET_RESUME_PREFIX}{application_id}.pdf"

    def get_video_key(self, video_verification_id):
        return f"{BUCKET_VIDEOS_PREFIX}{video_verification_id}"

    def delete_objects(self, bucket_name: str, keys: list[str]) -> None:
        if not keys:
            return
        response = s3_client.delete_objects(
            Bucket=bucket_name,
            Delete={"Objects": [{"Key": key} for key in keys], "Quiet": True},
        )
        if response.get("Errors"):
            raise RuntimeError(f"Failed to delete S3 objects: {response['Errors']}")
