from typing import List

from pydantic import BaseModel, Field

from .core import Response

MATCH_ID_PATTERN = r"^[0-9]{8}-[0-9]{2}-[0-9]{3}$"


class MatchReward(BaseModel):
    match_id: str = Field(regex=MATCH_ID_PATTERN)
    is_completed: bool

    class Config:
        orm_mode = True


class MatchChoice(BaseModel):
    match_id: str = Field(regex=MATCH_ID_PATTERN)
    choice: int = Field(ge=0, le=5, default=0)
    user_count: int = Field(gt=0, le=1000000, default=0)

    class Config:
        orm_mode = True


class Match(BaseModel):
    match_id: str = Field(regex=MATCH_ID_PATTERN)
    pitcher: str
    batter: str
    result: int = Field(ge=0, le=5, default=0)
    choices: List[int] = [0, 0, 0, 0, 0, 0]


class MatchResponse(Response):
    content: Match
