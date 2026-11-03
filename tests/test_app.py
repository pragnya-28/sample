from app.main import app


def test_homepage_renders():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"AI Resource Impact Monitor" in response.data


def test_health_endpoint():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_login_success():
    client = app.test_client()
    response = client.post(
        "/api/v1/login",
        json={"username": "ops-admin", "password": "admin123"},
    )
    assert response.status_code == 200
    assert response.get_json()["user"]["role"] == "admin"


def test_dashboard_requires_auth():
    client = app.test_client()
    response = client.get("/api/v1/dashboard")
    assert response.status_code == 401


def test_dashboard_after_login():
    client = app.test_client()
    client.post("/api/v1/login", json={"username": "ai-analyst", "password": "analyst123"})
    response = client.get("/api/v1/dashboard")
    assert response.status_code == 200
    body = response.get_json()
    assert "summary" in body
    assert "total_tokens" in body["summary"]


def test_audit_log_and_usage_create():
    client = app.test_client()
    client.post("/api/v1/login", json={"username": "ops-admin", "password": "admin123"})

    usage_response = client.post(
        "/api/v1/usage",
        json={
            "source": "openai",
            "team": "finops",
            "project": "document-summarizer",
            "model": "gpt-4o-mini",
            "requests": 120,
            "tokens": 85000,
            "compute_hours": 4.5,
            "region": "us-east-1",
            "status": "success",
        },
    )
    assert usage_response.status_code == 201

    audits_response = client.get("/api/v1/audits")
    assert audits_response.status_code == 200
    assert len(audits_response.get_json()["audit_events"]) >= 2
