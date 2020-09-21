from pydantic import BaseModel, Field

from .match import MATCH_ID_PATTERN
from .user import USER_ID_PATTERN


class Forcast(BaseModel):
    match_id: str = Field(regex=MATCH_ID_PATTERN)
    user_id: str = Field(regex=USER_ID_PATTERN)
    choice: int = Field(ge=0, le=5)
