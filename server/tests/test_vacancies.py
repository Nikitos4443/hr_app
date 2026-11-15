from starlette import status


def login(client, username):
    response = client.post("/auth/token", data={"username": username, "password": "secret123"})
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def setup_company(client, admin_name, company_name):
    """Register an admin, create their company and one HR. Returns (admin, hr) headers."""
    body = {"username": admin_name, "password": "secret123", "confirm_password": "secret123"}
    client.post("/auth/", json=body)
    admin = login(client, admin_name)
    client.post("/companies/", headers=admin, json={"name": company_name})
    hr_name = f"hr_{admin_name}"
    client.post("/users/", headers=admin, json={"username": hr_name, "password": "secret123"})
    return admin, login(client, hr_name)


def create_vacancy(client, headers, title="Python dev", **extra):
    return client.post("/vacancies/", headers=headers, json={"title": title, **extra})


def test_hr_creates_vacancy_in_own_company(client):
    admin, hr = setup_company(client, "boss", "Acme")

    response = create_vacancy(client, hr, responsibilities=["code"], salary_min=1000)

    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert body["title"] == "Python dev"
    assert body["company"] == "Acme"
    assert body["status"] == "open"
    assert body["responsibilities"] == ["code"]
    assert body["selection_status"] == "pending"
    # created_by is the HR who made it, company_id the shared company
    assert client.get(f"/vacancies/{body['id']}", headers=admin).status_code == 200


def test_admin_and_hr_see_the_same_company_vacancies(client):
    admin, hr = setup_company(client, "boss", "Acme")
    create_vacancy(client, admin, title="By admin")
    create_vacancy(client, hr, title="By hr")

    for headers in (admin, hr):
        titles = {v["title"] for v in client.get("/vacancies/", headers=headers).json()}
        assert titles == {"By admin", "By hr"}


def test_user_cannot_see_other_company_vacancies(client):
    admin, hr = setup_company(client, "boss", "Acme")
    other_admin, _ = setup_company(client, "boss2", "Globex")
    vacancy_id = create_vacancy(client, other_admin).json()["id"]

    assert client.get("/vacancies/", headers=admin).json() == []
    assert client.get(f"/vacancies/{vacancy_id}", headers=hr).status_code == 404
    patch = client.patch(f"/vacancies/{vacancy_id}", headers=admin, json={"title": "x"})
    assert patch.status_code == 404
    assert client.delete(f"/vacancies/{vacancy_id}", headers=admin).status_code == 404


def test_update_vacancy(client):
    _, hr = setup_company(client, "boss", "Acme")
    vacancy_id = create_vacancy(client, hr, location="Kyiv").json()["id"]

    response = client.patch(
        f"/vacancies/{vacancy_id}",
        headers=hr,
        json={"title": "Senior dev", "status": "closed", "requirements": ["python"]},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Senior dev"
    assert body["status"] == "closed"
    assert body["requirements"] == ["python"]
    assert body["location"] == "Kyiv"  # untouched


def test_update_can_clear_optional_field(client):
    _, hr = setup_company(client, "boss", "Acme")
    vacancy_id = create_vacancy(client, hr, location="Kyiv").json()["id"]

    response = client.patch(f"/vacancies/{vacancy_id}", headers=hr, json={"location": None})

    assert response.json()["location"] is None


def test_title_cannot_be_nulled(client):
    _, hr = setup_company(client, "boss", "Acme")
    vacancy_id = create_vacancy(client, hr).json()["id"]

    response = client.patch(f"/vacancies/{vacancy_id}", headers=hr, json={"title": None})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_salary_range_is_validated(client):
    _, hr = setup_company(client, "boss", "Acme")
    bad = create_vacancy(client, hr, salary_min=5000, salary_max=1000)
    assert bad.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    vacancy_id = create_vacancy(client, hr, salary_min=1000, salary_max=2000).json()["id"]
    patch = client.patch(f"/vacancies/{vacancy_id}", headers=hr, json={"salary_min": 3000})
    assert patch.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_invalid_status_and_empty_title_are_rejected(client):
    _, hr = setup_company(client, "boss", "Acme")

    assert create_vacancy(client, hr, status="weird").status_code == 422
    assert create_vacancy(client, hr, title="  ").status_code == 422


def test_delete_vacancy(client):
    _, hr = setup_company(client, "boss", "Acme")
    vacancy_id = create_vacancy(client, hr).json()["id"]

    assert client.delete(f"/vacancies/{vacancy_id}", headers=hr).status_code == 204
    assert client.get(f"/vacancies/{vacancy_id}", headers=hr).status_code == 404


def test_admin_without_company_cannot_use_vacancies(client):
    body = {"username": "boss", "password": "secret123", "confirm_password": "secret123"}
    client.post("/auth/", json=body)
    admin = login(client, "boss")

    assert client.get("/vacancies/", headers=admin).status_code == status.HTTP_403_FORBIDDEN
    assert create_vacancy(client, admin).status_code == status.HTTP_403_FORBIDDEN


def test_vacancies_require_authentication(client):
    assert client.get("/vacancies/").status_code == status.HTTP_401_UNAUTHORIZED
