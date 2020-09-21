from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.dialects import mysql
from sqlalchemy.types import CHAR

from .core import Base, DatetimeMixin


class UserByPointModel(DatetimeMixin, Base):
    __tablename__ = "app_user_by_point"

    id = Column(Integer, autoincrement=True, primary_key=True)
    point = Column(mysql.MEDIUMINT(7, unsigned=True), index=True, nullable=False)
    user_count = Column(mysql.MEDIUMINT(7, unsigned=True), server_default="0")
    match_id = Column(
        CHAR(15),
        ForeignKey("app_match.match_id", onupdate="RESTRICT", ondelete="RESTRICT"),
    )


class UserByDatetimeModel(DatetimeMixin, Base):
    __tablename__ = "app_user_by_datetime"

    aggregated_at = Column(DateTime, primary_key=True)
    user_count = Column(mysql.MEDIUMINT(7, unsigned=True), server_default="0")
