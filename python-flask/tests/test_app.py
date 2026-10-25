import json

import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_items_are_seeded_and_dates_serialised(client):
    r = client.get("/items")
    assert r.status_code == 200
    data = r.get_json()
    assert data["1"] == {"name": "Widget", "added": "2021-05-01"}
    assert data["2"]["added"] == "2021-06-12"


def test_keys_keep_their_order(client):
    body = client.get("/items").get_data(as_text=True)
    assert body.index('"name"') < body.index('"added"')  # JSON keys are not re-sorted


def test_banner_escapes_user_input(client):
    body = client.get("/banner?name=<script>x</script>").get_data(as_text=True)
    assert body == "<h1>Hello, &lt;script&gt;x&lt;/script&gt;</h1>"
    assert client.get("/banner").get_data(as_text=True) == "<h1>Hello, guest</h1>"


def test_export_downloads_csv(client):
    client.get("/items")  # make sure the data is seeded
    r = client.get("/export")
    assert r.status_code == 200
    assert r.mimetype == "text/csv"
    assert "attachment" in r.headers["Content-Disposition"] and "items.csv" in r.headers["Content-Disposition"]
    assert r.get_data(as_text=True).splitlines() == ["id,name", "1,Widget", "2,Gadget"]
