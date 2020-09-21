from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import relationship
from sqlalchemy.types import CHAR, VARCHAR

from .core import Base, DatetimeMixin


class MatchRewardModel(DatetimeMixin, Base):
    __tablename__ = "app_match_reward"

    id = Column(Integer, autoincrement=True, primary_key=True)
    match_id = Column(
        CHAR(15),
        ForeignKey("app_match.match_id", onupdate="RESTRICT", ondelete="RESTRICT"),
    )
    is_completed = Column(mysql.BOOLEAN, server_default="0")


class MatchChoiceModel(DatetimeMixin, Base):
    __tablename__ = "app_match_choice"

    id = Column(Integer, autoincrement=True, primary_key=True)
    match_id = Column(
        CHAR(15),
        ForeignKey("app_match.match_id", onupdate="RESTRICT", ondelete="RESTRICT"),
    )
    choice = Column(mysql.TINYINT(2, unsigned=True), index=True, server_default="0")
    user_count = Column(mysql.MEDIUMINT(7, unsigned=True), server_default="0")


class MatchModel(DatetimeMixin, Base):
    __tablename__ = "app_match"

    match_id = Column(CHAR(15), primary_key=True)
    pitcher = Column(VARCHAR(255), index=True, nullable=False)
    batter = Column(VARCHAR(255), index=True, nullable=False)
    result = Column(mysql.TINYINT(2, unsigned=True), server_default="0")

    forcastes = relationship("Forcast", backref="match")
    choices = relationship("MatchChoice", backref="match")
    raward = relationship("MatchChoice", backref="match")
