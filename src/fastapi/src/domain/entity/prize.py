from pydantic import BaseModel

from .core import Response


class Prize(BaseModel):
    keyword: str
    url: str


class PrizeResponse(Response):
    content: Prize
