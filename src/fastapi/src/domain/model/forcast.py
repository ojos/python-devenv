from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.dialects import mysql
from sqlalchemy.types import CHAR

from .core import Base, DatetimeMixin


class ForcastModel(DatetimeMixin, Base):
    __tablename__ = "app_forcast"

    id = Column(Integer, autoincrement=True, primary_key=True)
    match_id = Column(
        CHAR(15),
        ForeignKey("app_match.match_id", onupdate="RESTRICT", ondelete="RESTRICT"),
    )
    user_id = Column(
        CHAR(32),
        ForeignKey("app_user.user_id", onupdate="RESTRICT", ondelete="RESTRICT"),
    )
    choice = Column(mysql.TINYINT(2, unsigned=True), index=True, nullable=False)
    requested_at = Column(DateTime, nullable=False)
