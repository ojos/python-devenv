from typing import Optional

from sqlalchemy.orm import Session

from di.rdb import SqlalchemySessionFactory
from domain.config import settings
from domain.entity import User
from domain.model import UserModel
from infra.kvs.redis.aioredis import AioRedis
from intarface.repo.kvs.aioredis import (
    AioRedisListRepo,
    AioRedisSortedSetRepo,
    AioRedisStringRepo,
)
from intarface.repo.rdb.sqlalchemy import SqlalchemyOrmRepo
from usecase.serializer.core import BaseSerializer


class UserRedisRepoFactory(object):
    @staticmethod
    async def get() -> AioRedisStringRepo:
        client = await AioRedis.get(host=settings.CACHE_HOST)
        return AioRedisStringRepo(
            client=client,
            key_name="/app/user/{}",
            key_field="user_id",
            entity_cls=User,
            timeout=5 * 60,
        )


class UserListRedisRepoFactory(object):
    @staticmethod
    async def get() -> AioRedisListRepo:
        client = await AioRedis.get(host=settings.CACHE_HOST)
        return AioRedisListRepo(
            client=client,
            key_name="/app/user/list",
            key_field="user_id",
            entity_cls=User,
            timeout=5 * 60,
        )


class UserRdsRepoFactory(object):
    def get(client: Optional[Session] = None) -> AioRedisListRepo:
        if client is None:
            client = SqlalchemySessionFactory.get()
        return SqlalchemyOrmRepo(
            client=client,
            serializer=BaseSerializer,
            model_cls=UserModel,
        )


# class UserDatabaseRepoFactory(object):
#     @staticmethod
#     async def get() -> AioRedisStringRepo:
#         client = await Databases.get(
#             database="mysql",
#             port=3306,
#             user_name=settings.MYSQL_USER,
#             password=settings.MYSQL_PASSWORD,
#             db_name=settings.MYSQL_DATABASE,
#             host=settings.MYSQL_PRIMARY_HOST,
#         )
#         return AioRedisStringRepo(
#             client=client,
#             key_name="/app/user/{}",
#             key_field="user_id",
#             entity_cls=User,
#             timeout=5 * 60,
#         )


class UserScoreRepoFactory(object):
    @staticmethod
    async def get() -> AioRedisSortedSetRepo:
        client = await AioRedis.get(host=settings.CACHE_HOST)
        return AioRedisSortedSetRepo(
            client=client,
            key_name="/app/user/score",
            timeout=5 * 60,
        )
