import uuid

from pydantic import BaseModel, Field

from .core import Response

USER_ID_PATTERN = r"^[0-9a-f]{32}$"


def uuid4hex() -> str:
    return uuid.uuid4().hex


class UserInningPoint(BaseModel):
    user_id: str = Field(regex=USER_ID_PATTERN, default_factory=uuid4hex)
    inning: int = Field(gt=0, lt=100)
    point: int = Field(ge=0, le=1000, default=0)

    class Config:
        orm_mode = True


class User(BaseModel):
    # get request
    user_id: str = Field(regex=USER_ID_PATTERN, default_factory=uuid4hex)

    # post request
    name: str = Field(min_length=1, max_length=10, strip_whitespace=True)
    icon_id: str
    number: str = Field(regex=r"^\d{1,4}$")

    total_point: int = Field(ge=0, le=1000000, default=0)
    inning_point: int = Field(ge=0, le=1000, default=0)


class UserResponse(Response):
    content: User
