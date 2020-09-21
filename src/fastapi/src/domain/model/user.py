from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import relationship
from sqlalchemy.types import CHAR, VARCHAR

from .core import Base, DatetimeMixin


class UserInningPointModel(DatetimeMixin, Base):
    __tablename__ = "app_user_inning_point"

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(
        CHAR(32),
        ForeignKey("app_user.user_id", onupdate="RESTRICT", ondelete="RESTRICT"),
    )
    inning = Column(mysql.TINYINT(2, unsigned=True), index=True, server_default="0")
    point = Column(mysql.SMALLINT(4, unsigned=True), server_default="0")


class UserModel(DatetimeMixin, Base):
    __tablename__ = "app_user"

    user_id = Column(CHAR(32), primary_key=True)
    name = Column(VARCHAR(10), index=True, nullable=False)
    icon_id = Column(VARCHAR(255), nullable=False)
    number = Column(VARCHAR(4), nullable=False)
    total_point = Column(mysql.MEDIUMINT(7, unsigned=True), server_default="0")

    forcastes = relationship("Forcast", backref="user")
    inning_points = relationship("UserInningPoint", backref="user")
