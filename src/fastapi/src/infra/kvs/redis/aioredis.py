import aioredis
from aioredis import ConnectionsPool


class AioRedis(object):
    _pool = None

    @classmethod
    async def get(
        cls,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        min_size: int = 5,
        max_size: int = 10,
        *args,
        **kwargs
    ) -> ConnectionsPool:
        if cls._pool is None:
            cls._pool = await aioredis.create_redis_pool(
                address="redis://{}:{}".format(host, port),
                db=db,
                minsize=min_size,
                maxsize=max_size,
                *args,
                **kwargs
            )
        return cls._pool

    @classmethod
    async def close(cls):
        cls._pool.close()
        await cls._pool.wait_closed()
