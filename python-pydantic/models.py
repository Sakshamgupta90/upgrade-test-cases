from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, root_validator, validator


class Address(BaseModel):
    street: str
    city: str
    postcode: str = Field(..., regex=r"^\d{5}$")


class User(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int] = None
    tags: List[str] = []
    address: Optional[Address] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        anystr_strip_whitespace = True

    @validator("email")
    def email_must_contain_at(cls, v):
        if "@" not in v:
            raise ValueError("invalid email")
        return v.lower()

    @root_validator
    def check_age(cls, values):
        age = values.get("age")
        if age is not None and age < 0:
            raise ValueError("age must be positive")
        return values


def load_user(payload: dict) -> User:
    return User.parse_obj(payload)


def load_user_json(raw: str) -> User:
    return User.parse_raw(raw)


def to_json(user: User) -> str:
    return user.json(exclude_none=True)


def to_dict(user: User) -> dict:
    return user.dict(exclude={"created_at"})


def rename(user: User, name: str) -> User:
    return user.copy(update={"name": name})


def user_schema() -> dict:
    return User.schema()
