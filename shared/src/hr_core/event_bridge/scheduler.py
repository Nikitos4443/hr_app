import json
import logging
from datetime import UTC, datetime

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

SCHEDULE_NAME_PREFIX = "analyze-vacancy-"


class AnalyzerScheduler:
    def __init__(
        self,
        lambda_arn: str,
        role_arn: str,
        group_name: str = "default",
        client=None,
    ):
        self.lambda_arn = lambda_arn
        self.role_arn = role_arn
        self.group_name = group_name
        self.client = client or boto3.client("scheduler")

    @staticmethod
    def schedule_name(vacancy_id: int) -> str:
        return f"{SCHEDULE_NAME_PREFIX}{vacancy_id}"

    def schedule(self, vacancy_id: int, run_at: datetime) -> str:
        name = self.schedule_name(vacancy_id)
        params = self._schedule_params(name, vacancy_id, run_at)
        try:
            self.client.create_schedule(**params)
        except ClientError as e:
            if e.response["Error"]["Code"] != "ConflictException":
                raise
            self.client.update_schedule(**params)
            logger.info("Rescheduled analyzer for vacancy %s at %s", vacancy_id, run_at)
        else:
            logger.info("Scheduled analyzer for vacancy %s at %s", vacancy_id, run_at)
        return name

    def cancel(self, vacancy_id: int) -> None:
        try:
            self.client.delete_schedule(
                Name=self.schedule_name(vacancy_id), GroupName=self.group_name
            )
        except ClientError as e:
            if e.response["Error"]["Code"] != "ResourceNotFoundException":
                raise
            return
        logger.info("Cancelled analyzer schedule for vacancy %s", vacancy_id)

    def _schedule_params(self, name: str, vacancy_id: int, run_at: datetime) -> dict:
        if run_at.tzinfo is None:
            raise ValueError("run_at must be timezone-aware")
        run_at = run_at.astimezone(UTC)
        if run_at <= datetime.now(UTC):
            raise ValueError("run_at must be in the future")
        return {
            "Name": name,
            "GroupName": self.group_name,
            "ScheduleExpression": f"at({run_at:%Y-%m-%dT%H:%M:%S})",
            "ScheduleExpressionTimezone": "UTC",
            "FlexibleTimeWindow": {"Mode": "OFF"},
            "ActionAfterCompletion": "DELETE",
            "Target": {
                "Arn": self.lambda_arn,
                "RoleArn": self.role_arn,
                "Input": json.dumps({"vacancy_id": vacancy_id}),
            },
        }
