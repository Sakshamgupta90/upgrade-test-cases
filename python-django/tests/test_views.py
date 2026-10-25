import json

import pytest
from django.test import Client


@pytest.fixture
def client():
    from notes import views
    views.NOTES.clear()
    return Client()


def post(client, text, ajax=True):
    headers = {"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"} if ajax else {}
    return client.post("/notes/", data=json.dumps({"text": text}), content_type="application/json", **headers)


def test_ajax_post_creates_a_note(client):
    r = post(client, "buy milk")
    assert r.status_code == 201 and r.json() == {"ok": True}
    notes = client.get("/notes/").json()["notes"]
    assert [n["text"] for n in notes] == ["buy milk"]
    assert notes[0]["created"].endswith("+00:00")  # stored in UTC


def test_non_ajax_post_is_rejected(client):
    r = post(client, "nope", ajax=False)
    assert r.status_code == 400
    assert r.content.decode() == "Expected an AJAX request"


def test_note_detail(client):
    post(client, "first")
    assert client.get("/notes/0/").json()["text"] == "first"
    r = client.get("/notes/5/")
    assert r.status_code == 404 and r.json() == {"error": "Not found"}


def test_other_methods_not_allowed(client):
    assert client.delete("/notes/").status_code == 405
