from datetime import UTC, datetime, timedelta

from hr_core.sql.tables.applications import Applications
from hr_core.sql.tables.evaluations import Evaluations
from hr_core.sql.tables.resume_verification import ResumeVerification
from hr_core.sql.tables.vacancies import Vacancies
from tests.test_vacancies import create_vacancy, setup_company

VIDEO_Q = {"type": "video", "text": "Tell us about yourself", "video_max_duration_sec": 60}
TEXT_Q = {"type": "text", "text": "Why us?", "video_max_duration_sec": None}


def seed_application(
    session_factory, vacancy_id, email, *, resume_score=80, invited=False, **extra
):
    with session_factory() as db:
        row = Applications(vacancy_id=vacancy_id, email=email, **extra)
        if invited:
            row.screening_invited_at = datetime.now(UTC)
        db.add(row)
        db.commit()
        db.add(
            ResumeVerification(
                application_id=row.id,
                status="done" if resume_score is not None else "pending",
                score=resume_score,
                llm_review={"is_resume": True, "score": resume_score, "description": "Solid"},
                processed_at=datetime.now(UTC),
            )
        )
        db.commit()
        return row.id, row.screening_token


# ---- public vacancy + apply ------------------------------------------------------------


def test_public_vacancy_hides_internal_fields_and_serves_closed(client):
    _, hr = setup_company(client, "boss", "Acme")
    vacancy_id = create_vacancy(client, hr, status="closed", description="d").json()["id"]

    response = client.get(f"/vacancies/public/{vacancy_id}")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "closed" and body["company"] == "Acme"
    assert not {"created_by", "company_id", "selection_status"} & body.keys()
    assert client.get("/vacancies/public/9999").status_code == 404


def test_apply_rejects_closed_expired_missing_and_duplicate(client, session_factory):
    _, hr = setup_company(client, "boss", "Acme")
    open_id = create_vacancy(client, hr).json()["id"]
    closed_id = create_vacancy(client, hr, status="closed").json()["id"]
    expired_id = create_vacancy(client, hr).json()["id"]
    with session_factory() as db:
        db.get(Vacancies, expired_id).deadline_at = datetime.now(UTC) - timedelta(days=1)
        db.commit()
    url = "/flow/resume-get-presigned-post-url"

    assert client.post(url, json={"vacancy_id": 9999, "email": "a@x.com"}).status_code == 404
    assert client.post(url, json={"vacancy_id": closed_id, "email": "a@x.com"}).status_code == 409
    assert client.post(url, json={"vacancy_id": expired_id, "email": "a@x.com"}).status_code == 409

    first = client.post(url, json={"vacancy_id": open_id, "email": "A@x.com"})
    assert first.status_code == 201
    duplicate = client.post(url, json={"vacancy_id": open_id, "email": "a@X.com"})
    assert duplicate.status_code == 409
    assert "already applied" in duplicate.json()["detail"]


def test_failed_presign_does_not_lock_candidate_out(client, fake_s3):
    _, hr = setup_company(client, "boss", "Acme")
    vacancy_id = create_vacancy(client, hr).json()["id"]
    url = "/flow/resume-get-presigned-post-url"
    body = {"vacancy_id": vacancy_id, "email": "a@x.com"}

    fake_s3.fail_post = True
    assert client.post(url, json=body).status_code == 502
    fake_s3.fail_post = False
    assert client.post(url, json=body).status_code == 201


# ---- questions -------------------------------------------------------------------------


def test_questions_replace_and_validation(client):
    admin, hr = setup_company(client, "boss", "Acme")
    other_admin, _ = setup_company(client, "boss2", "Globex")
    vid = create_vacancy(client, hr).json()["id"]

    put = client.put(f"/vacancies/{vid}/questions", headers=hr, json=[VIDEO_Q, TEXT_Q])
    assert put.status_code == 200
    assert [(q["order"], q["type"]) for q in put.json()] == [(1, "video"), (2, "text")]
    assert client.get(f"/vacancies/{vid}", headers=hr).json()["questions_count"] == 2

    replaced = client.put(f"/vacancies/{vid}/questions", headers=hr, json=[TEXT_Q])
    assert [q["text"] for q in client.get(f"/vacancies/{vid}/questions", headers=hr).json()] == [
        "Why us?"
    ]
    assert replaced.status_code == 200

    bad = [
        [{"type": "text", "text": "  ", "video_max_duration_sec": None}],
        [{"type": "video", "text": "q", "video_max_duration_sec": 5}],
        [{"type": "video", "text": "q", "video_max_duration_sec": 99999}],
        [{"type": "video", "text": "q"}],
        [{"type": "text", "text": "q", "video_max_duration_sec": 30}],
    ]
    for payload in bad:
        assert (
            client.put(f"/vacancies/{vid}/questions", headers=hr, json=payload).status_code == 422
        )
    assert client.get(f"/vacancies/{vid}/questions", headers=other_admin).status_code == 404


def test_questions_locked_once_candidates_answered(client, session_factory):
    _, hr = setup_company(client, "boss", "Acme")
    vid = create_vacancy(client, hr).json()["id"]
    client.put(f"/vacancies/{vid}/questions", headers=hr, json=[TEXT_Q])
    _, token = seed_application(session_factory, vid, "c@x.com", invited=True)
    question_id = client.get(f"/flow/screening/{token}").json()["questions"][0]["id"]
    assert (
        client.put(
            f"/flow/screening/{token}/questions/{question_id}/text-answer",
            json={"answer": "Because"},
        ).status_code
        == 200
    )

    locked = client.put(f"/vacancies/{vid}/questions", headers=hr, json=[VIDEO_Q])
    assert locked.status_code == 409


# ---- candidate screening ---------------------------------------------------------------


def test_screening_view_and_error_codes(client, session_factory):
    _, hr = setup_company(client, "boss", "Acme")
    vid = create_vacancy(client, hr, title="Dev").json()["id"]
    client.put(f"/vacancies/{vid}/questions", headers=hr, json=[VIDEO_Q, TEXT_Q])
    _, token = seed_application(session_factory, vid, "c@x.com", invited=True)
    _, not_invited = seed_application(session_factory, vid, "n@x.com")
    pending_id, pending_token = seed_application(
        session_factory, vid, "p@x.com", invited=True, resume_score=None
    )
    rejected_id, rejected_token = seed_application(
        session_factory, vid, "r@x.com", invited=True, status="rejected"
    )
    purged_id, purged_token = seed_application(
        session_factory, vid, "g@x.com", status="rejected", purged_at=datetime.now(UTC)
    )

    view = client.get(f"/flow/screening/{token}")
    assert view.status_code == 200
    body = view.json()
    assert body["vacancy_title"] == "Dev" and body["company_name"] == "Acme"
    assert body["screening_progress"] == "in_progress"
    assert [q["answered"] for q in body["questions"]] == [False, False]
    assert set(body) == {
        "vacancy_title",
        "company_name",
        "status",
        "screening_progress",
        "questions",
    }

    qid = body["questions"][1]["id"]
    client.put(f"/flow/screening/{token}/questions/{qid}/text-answer", json={"answer": "x"})
    assert client.get(f"/flow/screening/{token}").json()["questions"][1]["answered"] is True

    assert client.get("/flow/screening/nope").status_code == 404
    assert client.get(f"/flow/screening/{not_invited}").status_code == 403
    assert client.get(f"/flow/screening/{rejected_token}").status_code == 403
    assert client.get(f"/flow/screening/{purged_token}").status_code == 410
    assert client.get(f"/flow/screening/{pending_token}").status_code == 409


def test_screening_completed_when_everything_answered(client, session_factory):
    _, hr = setup_company(client, "boss", "Acme")
    vid = create_vacancy(client, hr).json()["id"]
    client.put(f"/vacancies/{vid}/questions", headers=hr, json=[TEXT_Q])
    _, token = seed_application(session_factory, vid, "c@x.com", invited=True)
    qid = client.get(f"/flow/screening/{token}").json()["questions"][0]["id"]
    client.put(f"/flow/screening/{token}/questions/{qid}/text-answer", json={"answer": "x"})

    assert client.get(f"/flow/screening/{token}").json()["screening_progress"] == "completed"


# ---- staff: list, detail, actions -------------------------------------------------------


def test_applications_list_filters_sorts_and_counts(client, session_factory):
    admin, hr = setup_company(client, "boss", "Acme")
    vid = create_vacancy(client, hr).json()["id"]
    client.put(f"/vacancies/{vid}/questions", headers=hr, json=[TEXT_Q])
    a, _ = seed_application(
        session_factory, vid, "alice@x.com", resume_score=90, full_name="Alice A"
    )
    b, _ = seed_application(session_factory, vid, "bob@x.com", resume_score=60, invited=True)
    seed_application(session_factory, vid, "carl@x.com", resume_score=30, status="rejected")
    with session_factory() as db:
        db.add(Evaluations(application_id=b, vacancy_id=vid, order=1, summary="Top"))
        db.commit()

    body = client.get(f"/vacancies/{vid}/applications", headers=hr).json()
    assert body["total"] == 3
    assert body["counts"] == {"all": 3, "pending": 1, "invited": 1, "shortlisted": 0, "rejected": 1}
    by_email = {i["email"]: i for i in body["items"]}
    assert by_email["bob@x.com"]["rank"] == 1 and by_email["bob@x.com"]["ai_summary"] == "Top"
    assert by_email["bob@x.com"]["screening_state"] == "invited"
    assert by_email["alice@x.com"]["screening_state"] == "not_invited"
    assert by_email["alice@x.com"]["total_questions"] == 1

    by_score = client.get(
        f"/vacancies/{vid}/applications?sort=resume_score&order=desc", headers=hr
    ).json()
    assert [i["resume_score"] for i in by_score["items"]] == [90, 60, 30]

    invited = client.get(f"/vacancies/{vid}/applications?status=invited", headers=hr).json()
    assert [i["email"] for i in invited["items"]] == ["bob@x.com"]
    assert invited["counts"]["all"] == 3  # counts ignore the current filter

    found = client.get(f"/vacancies/{vid}/applications?search=ALICE", headers=hr).json()
    assert [i["id"] for i in found["items"]] == [a]
    assert client.get(f"/vacancies/{vid}/applications?search=%25", headers=hr).json()["total"] == 0

    page = client.get(f"/vacancies/{vid}/applications?limit=1&offset=1", headers=hr).json()
    assert len(page["items"]) == 1 and page["total"] == 3


def test_application_detail_has_resume_answers_and_timeline(client, session_factory, fake_s3):
    _, hr = setup_company(client, "boss", "Acme")
    vid = create_vacancy(client, hr).json()["id"]
    client.put(f"/vacancies/{vid}/questions", headers=hr, json=[TEXT_Q])
    app_id, token = seed_application(session_factory, vid, "c@x.com", invited=True)
    qid = client.get(f"/flow/screening/{token}").json()["questions"][0]["id"]
    client.put(f"/flow/screening/{token}/questions/{qid}/text-answer", json={"answer": "Because"})

    body = client.get(f"/applications/{app_id}", headers=hr).json()

    assert body["resume"]["review"] == {"is_resume": True, "score": 80.0, "description": "Solid"}
    assert body["resume"]["file_url"] == f"https://s3.test/test-bucket/CV/{app_id}.pdf?signed"
    assert body["answers"] == [
        {
            "question_id": qid,
            "order": 1,
            "type": "text",
            "text": "Why us?",
            "status": "done",
            "answer": "Because",
            "transcription": None,
        }
    ]
    assert {e["type"] for e in body["timeline"]} == {
        "applied",
        "resume_processed",
        "screening_invited",
        "screening_completed",
    }


def test_applications_of_other_company_are_hidden(client, session_factory):
    _, hr = setup_company(client, "boss", "Acme")
    other_admin, _ = setup_company(client, "boss2", "Globex")
    vid = create_vacancy(client, hr).json()["id"]
    app_id, _ = seed_application(session_factory, vid, "c@x.com")

    assert client.get(f"/applications/{app_id}", headers=other_admin).status_code == 404
    assert client.post(f"/applications/{app_id}/reject", headers=other_admin).status_code == 404
    assert client.get(f"/vacancies/{vid}/applications", headers=other_admin).status_code == 404


def test_invite_sends_mail_once_and_is_idempotent(client, session_factory, fake_channel):
    _, hr = setup_company(client, "boss", "Acme")
    vid = create_vacancy(client, hr).json()["id"]
    app_id, token = seed_application(session_factory, vid, "c@x.com")
    not_ready, _ = seed_application(session_factory, vid, "n@x.com", resume_score=None)

    first = client.post(f"/applications/{app_id}/invite", headers=hr)
    again = client.post(f"/applications/{app_id}/invite", headers=hr)

    assert first.status_code == again.status_code == 200
    assert first.json()["status"] == "invited"
    assert len(fake_channel.sent) == 1
    assert f"/screening/{token}" in fake_channel.sent[0][2]
    assert client.post(f"/applications/{not_ready}/invite", headers=hr).status_code == 409


def test_invite_mail_failure_keeps_application_uninvited(client, session_factory, fake_channel):
    _, hr = setup_company(client, "boss", "Acme")
    vid = create_vacancy(client, hr).json()["id"]
    app_id, _ = seed_application(session_factory, vid, "c@x.com")
    fake_channel.fail = True

    assert client.post(f"/applications/{app_id}/invite", headers=hr).status_code == 502
    fake_channel.fail = False
    assert client.post(f"/applications/{app_id}/invite", headers=hr).json()["status"] == "invited"


def test_shortlist_and_reject_transitions(client, session_factory, fake_channel, fake_s3):
    _, hr = setup_company(client, "boss", "Acme")
    vid = create_vacancy(client, hr).json()["id"]
    app_id, _ = seed_application(session_factory, vid, "c@x.com", full_name="Cee")

    shortlisted = client.post(f"/applications/{app_id}/shortlist", headers=hr)
    assert shortlisted.json()["status"] == "shortlisted"
    assert client.post(f"/applications/{app_id}/shortlist", headers=hr).status_code == 200
    assert client.post(f"/applications/{app_id}/invite", headers=hr).status_code == 409

    rejected = client.post(f"/applications/{app_id}/reject", headers=hr)
    assert rejected.status_code == 200 and rejected.json()["status"] == "rejected"
    assert client.post(f"/applications/{app_id}/reject", headers=hr).status_code == 200
    assert client.post(f"/applications/{app_id}/shortlist", headers=hr).status_code == 409

    assert len(fake_channel.sent) == 1  # one rejection mail, not repeated
    assert f"CV/{app_id}.pdf" in fake_s3.deleted
    with session_factory() as db:
        row = db.get(Applications, app_id)
        assert row.rejection_notified_at is not None
        assert row.purged_at is not None and row.full_name is None


def test_bulk_action_reports_partial_failures(client, session_factory):
    _, hr = setup_company(client, "boss", "Acme")
    vid = create_vacancy(client, hr).json()["id"]
    other_vid = create_vacancy(client, hr, title="Other").json()["id"]
    ok, _ = seed_application(session_factory, vid, "a@x.com")
    rejected, _ = seed_application(session_factory, vid, "b@x.com", status="rejected")
    foreign, _ = seed_application(session_factory, other_vid, "c@x.com")

    response = client.post(
        f"/vacancies/{vid}/applications/bulk",
        headers=hr,
        json={"ids": [ok, rejected, foreign, 9999], "action": "shortlist"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["updated"] == [ok]
    assert {f["id"]: f["detail"] for f in body["failed"]} == {
        rejected: "Application was rejected",
        foreign: "Application not found",
        9999: "Application not found",
    }


# ---- vacancies and users ---------------------------------------------------------------


def test_vacancy_counts_and_retry_selection(client, session_factory, fake_scheduler):
    admin, hr = setup_company(client, "boss", "Acme")
    vid = create_vacancy(client, hr).json()["id"]
    seed_application(session_factory, vid, "a@x.com")
    seed_application(session_factory, vid, "b@x.com")

    listed = client.get("/vacancies/", headers=hr).json()
    assert listed[0]["applications_count"] == 2 and listed[0]["questions_count"] == 0

    assert client.post(f"/vacancies/{vid}/retry-selection", headers=hr).status_code == 409
    with session_factory() as db:
        db.get(Vacancies, vid).selection_status = "failed"
        db.commit()
    retried = client.post(f"/vacancies/{vid}/retry-selection", headers=hr)
    assert retried.status_code == 200
    assert retried.json()["selection_status"] == "pending"
    assert vid in fake_scheduler.scheduled
    assert client.post(f"/vacancies/{vid}/retry-selection", headers=hr).status_code == 409


def test_users_expose_created_at(client):
    admin, _ = setup_company(client, "boss", "Acme")
    users = client.get("/users/", headers=admin).json()
    assert users and all(u["created_at"] for u in users)
