from datetime import datetime, timezone
from typing import List, Optional, Annotated

from pydantic import BaseModel, Field, model_validator, field_validator, validate_call
from pydantic import ValidationInfo


class Address(BaseModel):
    street: str
    city: str
    postcode: str = Field(..., pattern=r"^\d{5}$")


class User(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int] = None
    tags: List[Annotated[str, Field(min_length=1)]] = []
    address: Optional[Address] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {
        "from_attributes": True,
        "validate_by_name": True,
        "str_strip_whitespace": True,
    }

    @field_validator("email", mode="before")
    @classmethod
    def email_must_contain_at(cls, v: str, info: ValidationInfo) -> str:
        if "@" not in v:
            raise ValueError("invalid email")
        return v.lower()

    @model_validator(mode="after")
    def check_age(self) -> "User":
        if self.age is not None and self.age < 0:
            raise ValueError("age must be positive")
        return self


@validate_call
def load_user(payload: dict) -> User:
    return User.model_validate(payload)


@validate_call
def load_user_json(raw: str) -> User:
    return User.model_validate_json(raw)


@validate_call
def to_json(user: User) -> str:
    return user.model_dump_json(exclude_none=True)


@validate_call
def to_dict(user: User) -> dict:
    return user.model_dump(exclude={"created_at"})


@validate_call
def rename(user: User, name: str) -> User:
    return user.model_copy(update={"name": name})


@validate_call
def user_schema() -> dict:
    return User.model_json_schema()
