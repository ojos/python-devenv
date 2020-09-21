from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from domain.config import settings
from domain.model import Base
from infra.rdb.sqlarchemy import SqlalcemyEngine
from intarface.command.rdb import RdbCommand
from usecase.interactor import (
    CreateTableInteractor,
    DropTableInteractor,
    ITableInteractor,
)


class SqlalchemyEngineFactory(object):
    @staticmethod
    def get() -> Engine:
        engine: Engine = SqlalcemyEngine.get(
            engine="mysql",
            port=3306,
            user_name=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            db=settings.MYSQL_DATABASE,
            host=settings.MYSQL_PRIMARY_HOST,
        )
        return engine


class SqlalchemySessionFactory(object):
    @staticmethod
    def get(autocommit: bool = False, autoflush: bool = True) -> Session:
        engine: Engine = SqlalchemyEngineFactory.get()
        session: Session = sessionmaker(
            autocommit=autocommit, autoflush=autoflush, bind=engine
        )()
        return session


class CreateTableInteractorFactory(object):
    @staticmethod
    def get() -> ITableInteractor:
        engine: Engine = SqlalchemyEngineFactory.get()
        return CreateTableInteractor(engine, Base)


class DropTableInteractorFactory(object):
    @staticmethod
    def get() -> ITableInteractor:
        engine: Engine = SqlalchemyEngineFactory.get()
        return DropTableInteractor(engine, Base)


class RdbCommandFactory(object):
    @staticmethod
    def get() -> RdbCommand:
        return RdbCommand(
            create_table_interactor=CreateTableInteractorFactory.get(),
            drop_table_interactor=DropTableInteractorFactory.get(),
        )
