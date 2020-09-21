from datetime import datetime

from pydantic import BaseModel, Field

from .match import MATCH_ID_PATTERN


class UserByPoint(BaseModel):
    match_id: str = Field(regex=MATCH_ID_PATTERN)
    point: int = Field(gt=0, le=1000000)
    user_count: int = Field(gt=0, le=1000000)

    class Config:
        orm_mode = True


class UserByDatetime(BaseModel):
    aggregated_at: datetime
    user_count: int = Field(gt=0, le=1000000)

    class Config:
        orm_mode = True
