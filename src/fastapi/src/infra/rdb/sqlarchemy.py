from typing import Optional

from sqlalchemy.engine import Engine, create_engine


class SqlalcemyEngine(object):
    _engine: Optional[Engine] = None

    @classmethod
    def get(
        cls,
        engine: str,
        port: int,
        user_name: str,
        password: str,
        db: str,
        host: str = "localhost",
        pool_size: int = 5,
        max_overflow: int = 5,
        *args,
        **kwargs
    ) -> Engine:
        if cls._engine is None:
            url = "{}://{}:{}@{}:{}/{}".format(
                engine, user_name, password, host, port, db
            )
            cls._engine = create_engine(
                url, pool_size=pool_size, max_overflow=max_overflow, **kwargs
            )
        return cls._engine

    @classmethod
    def close(cls):
        cls._engine.dispose()
