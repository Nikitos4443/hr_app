import json
from datetime import UTC, datetime, timedelta, timezone

import boto3
import pytest
from botocore.stub import Stubber

from hr_core.event_bridge import AnalyzerScheduler

LAMBDA_ARN = "arn:aws:lambda:eu-central-1:123456789012:function:analyzer"
ROLE_ARN = "arn:aws:iam::123456789012:role/scheduler"


@pytest.fixture
def scheduler_client():
    client = boto3.client(
        "scheduler",
        region_name="eu-central-1",
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )
    with Stubber(client) as stubber:
        yield client, stubber
        stubber.assert_no_pending_responses()


def make_scheduler(client):
    return AnalyzerScheduler(lambda_arn=LAMBDA_ARN, role_arn=ROLE_ARN, client=client)


def expected_params(run_at_utc: str):
    return {
        "Name": "analyze-vacancy-7",
        "GroupName": "default",
        "ScheduleExpression": f"at({run_at_utc})",
        "ScheduleExpressionTimezone": "UTC",
        "FlexibleTimeWindow": {"Mode": "OFF"},
        "ActionAfterCompletion": "DELETE",
        "Target": {
            "Arn": LAMBDA_ARN,
            "RoleArn": ROLE_ARN,
            "Input": json.dumps({"vacancy_id": 7}),
        },
    }


def test_schedule_creates_one_off_schedule_in_utc(scheduler_client):
    client, stubber = scheduler_client
    run_at = (datetime.now(UTC) + timedelta(days=1)).replace(microsecond=0)
    local = run_at.astimezone(timezone(timedelta(hours=2)))
    stubber.add_response(
        "create_schedule",
        {"ScheduleArn": "arn:aws:scheduler:::schedule/default/analyze-vacancy-7"},
        expected_params(f"{run_at:%Y-%m-%dT%H:%M:%S}"),
    )

    name = make_scheduler(client).schedule(7, local)

    assert name == "analyze-vacancy-7"


def test_schedule_updates_when_already_scheduled(scheduler_client):
    client, stubber = scheduler_client
    run_at = (datetime.now(UTC) + timedelta(days=1)).replace(microsecond=0)
    params = expected_params(f"{run_at:%Y-%m-%dT%H:%M:%S}")
    stubber.add_client_error("create_schedule", "ConflictException", expected_params=params)
    stubber.add_response(
        "update_schedule",
        {"ScheduleArn": "arn:aws:scheduler:::schedule/default/analyze-vacancy-7"},
        params,
    )

    make_scheduler(client).schedule(7, run_at)


def test_schedule_propagates_other_errors(scheduler_client):
    client, stubber = scheduler_client
    stubber.add_client_error("create_schedule", "AccessDeniedException")

    with pytest.raises(Exception, match="AccessDenied"):
        make_scheduler(client).schedule(7, datetime.now(UTC) + timedelta(days=1))


def test_schedule_rejects_naive_and_past_times(scheduler_client):
    client, _ = scheduler_client
    scheduler = make_scheduler(client)

    with pytest.raises(ValueError, match="timezone-aware"):
        scheduler.schedule(7, datetime.now() + timedelta(days=1))
    with pytest.raises(ValueError, match="future"):
        scheduler.schedule(7, datetime.now(UTC) - timedelta(minutes=1))


def test_cancel_deletes_schedule(scheduler_client):
    client, stubber = scheduler_client
    stubber.add_response(
        "delete_schedule", {}, {"Name": "analyze-vacancy-7", "GroupName": "default"}
    )

    make_scheduler(client).cancel(7)


def test_cancel_ignores_missing_schedule(scheduler_client):
    client, stubber = scheduler_client
    stubber.add_client_error("delete_schedule", "ResourceNotFoundException")

    make_scheduler(client).cancel(7)
