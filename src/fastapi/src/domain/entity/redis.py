from pydantic import BaseModel


class RedisSortedSet(BaseModel):
    member: str
    score: int
