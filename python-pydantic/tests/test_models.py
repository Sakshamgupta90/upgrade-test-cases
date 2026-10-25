import json
from datetime import datetime
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from models import load_user, load_user_json, rename, to_dict, to_json, user_schema

ADA = {"id": 1, "name": "  Ada  ", "email": "ADA@Example.com", "tags": ["admin"],
       "address": {"street": "1 Main St", "city": "London", "postcode": "12345"}}


def test_load_cleans_fields():
    user = load_user(ADA)
    assert user.name == "Ada"
    assert user.email == "ada@example.com"
    assert user.address.city == "London"
    assert isinstance(user.created_at, datetime)


def test_invalid_input_is_rejected():
    for bad in ({**ADA, "email": "nope"}, {**ADA, "age": -1},
                {**ADA, "address": {**ADA["address"], "postcode": "ABC"}}):
        with pytest.raises(ValidationError):
            load_user(bad)


def test_load_from_json():
    assert load_user_json(json.dumps(ADA)).id == 1


def test_from_attributes_and_field_names():
    from models import User
    record = SimpleNamespace(id=2, name="Linus", email="l@example.com", age=30, tags=[], address=None,
                             created_at=datetime(2020, 1, 1))
    loader = getattr(User, "model_validate", None) or User.from_orm
    assert loader(record).age == 30


def test_dump_helpers():
    user = load_user(ADA)
    data = to_dict(user)
    assert "created_at" not in data and data["tags"] == ["admin"]
    dumped = json.loads(to_json(user))
    assert "age" not in dumped and dumped["email"] == "ada@example.com"


def test_rename_returns_a_copy():
    user = load_user(ADA)
    assert rename(user, "Grace").name == "Grace" and user.name == "Ada"


def test_schema_describes_the_model():
    schema = user_schema()
    assert schema["title"] == "User"
    assert {"id", "name", "email"} <= set(schema["properties"])
