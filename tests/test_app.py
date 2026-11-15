import os
import tempfile
import pytest

os.environ["DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test.db")

import app as app_module  # noqa: E402


@pytest.fixture
def client():
    flask_app = app_module.create_app()
    flask_app.config["TESTING"] = True
    return flask_app.test_client()


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_add_and_view_note(client):
    client.post("/add", data={"title": "CC", "content": "CI/CD notes"})
    r = client.get("/")
    assert b"CI/CD notes" in r.data


def test_edit_note(client):
    client.post("/add", data={"title": "Old", "content": "old text"})
    with app_module.get_db() as conn:
        nid = conn.execute("SELECT id FROM notes WHERE title='Old'").fetchone()["id"]
    client.post(f"/edit/{nid}", data={"title": "New", "content": "new text"})
    assert b"new text" in client.get("/").data


def test_delete_note(client):
    client.post("/add", data={"title": "Temp", "content": "delete me"})
    with app_module.get_db() as conn:
        nid = conn.execute("SELECT id FROM notes WHERE title='Temp'").fetchone()["id"]
    client.post(f"/delete/{nid}")
    assert b"delete me" not in client.get("/").data
