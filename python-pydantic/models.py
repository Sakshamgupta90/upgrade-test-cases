from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class Address(BaseModel):
    street: str
    city: str
    postcode: str = Field(..., pattern=r"^\d{5}$")


class User(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int] = None
    tags: List[str] = Field(default_factory=list)
    address: Optional[Address] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        str_strip_whitespace=True,
    )

    @field_validator("email")
    def email_must_contain_at(cls, v):
        if "@" not in v:
            raise ValueError("invalid email")
        return v.lower()

    @model_validator(mode="after")
    def check_age(self):
        if self.age is not None and self.age < 0:
            raise ValueError("age must be positive")
        return self


def load_user(payload: dict) -> User:
    return User.model_validate(payload)


def load_user_json(raw: str) -> User:
    return User.model_validate_json(raw)


def to_json(user: User) -> str:
    return user.model_dump_json(exclude_none=True)


def to_dict(user: User) -> dict:
    return user.model_dump(exclude={"created_at"})


def rename(user: User, name: str) -> User:
    return user.model_copy(update={"name": name})


def user_schema() -> dict:
    return User.model_json_schema()
