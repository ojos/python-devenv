from datetime import datetime

from ojos.conv.datetime import as_tz
from pydantic import BaseModel, Field

from domain.config import settings


def now() -> datetime:
    return as_tz(datetime.utcnow(), settings.TIMEZONE)


class Response(BaseModel):
    code: int = Field(200, ge=200, lt=600)
    message: str = "OK"
    servertime: datetime = Field(default_factory=now)
