from typing import Optional

from databases import Database


class Databases(object):
    _pool: Optional[Database] = None

    @classmethod
    async def get(
        cls,
        engine: str,
        port: int,
        user_name: str,
        password: str,
        db: str,
        host: str = "localhost",
        min_size: int = 5,
        max_size: int = 10,
        # pool_recycle: int = -1,  # connecttion timeout sceconds
        # echo: bool = False,  # print query
        *args,
        **kwargs
    ) -> Database:
        if cls._pool is None:
            url = "{}://{}:{}@{}:{}/{}".format(
                engine, user_name, password, host, port, db
            )
            cls._pool = Database(url, min_size=min_size, max_size=max_size, **kwargs)
            await cls._pool.connect()
        return cls._pool

    @classmethod
    async def close(cls):
        await cls._pool.disconnect()
