from sqlalchemy import Column, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.sql.functions import current_timestamp

Base: DeclarativeMeta = declarative_base()


class DatetimeMixin(object):
    __table_args__ = {
        "mysql_charset": "utf8mb4",
        "mysql_row_format": "DYNAMIC",
        "mysql_engine": "InnoDB",
    }

    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )
