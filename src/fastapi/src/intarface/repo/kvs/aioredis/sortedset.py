from typing import Any, Callable, Dict, List, Optional, Tuple

from aioredis import ConnectionsPool
from aioredis.commands.transaction import Pipeline

from domain.entity import RedisSortedSet
from intarface.repo import IAioDataStoreRepo

from .core import AioRedisRepo


class AioRedisSortedSetRepo(IAioDataStoreRepo, AioRedisRepo):
    def __init__(
        self,
        client: ConnectionsPool,
        key_name: str = "app/key_name",
        timeout: int = 60 * 3,
        *args,
        **kwargs
    ):
        super(AioRedisSortedSetRepo, self).__init__(
            client=client,
            key_name=key_name,
            timeout=timeout,
            key_field="member",
            entity_cls=RedisSortedSet,
        )

    async def find_all(
        self, reverse: bool = False, count: int = -1, *args, **kwargs
    ) -> List[RedisSortedSet]:
        _range: Callable = self._client.zrevrange if reverse else self._client.zrange
        entities: List[RedisSortedSet] = [
            self.entity_cls.parse_obj({"member": member, "score": score})
            for member, score in await _range(
                self.key_name, start=0, stop=count, withscores=True
            )
        ]
        return entities

    async def find_by(
        self,
        conditions: Dict[str, Any],
        reverse: bool = False,
        count: int = -1,
        *args,
        **kwargs
    ) -> List[RedisSortedSet]:
        entities: List[RedisSortedSet] = await self.find_all(
            reverse=reverse, count=count
        )
        if len(entities) > 0:
            for key, val in conditions.items():
                entities = [e for e in entities if getattr(e, key) == val]
        return entities

    async def count_by(
        self, conditions: Optional[Dict[str, str]] = None, *args, **kwargs
    ) -> int:
        if conditions is None:
            return await self._client.zcard(self.key_name)
        else:
            return len(await self.find_by(conditions))

    async def find_by_key(self, key: str, *args, **kwargs) -> Optional[RedisSortedSet]:
        score: Optional[int] = await self._client.zscore(self.key_name, key)
        if score is None:
            return None
        return self.entity_cls.parse_obj({"member": key, "score": score})

    async def create(self, entity: RedisSortedSet, *args, **kwargs) -> RedisSortedSet:
        entity, _ = await self.update_or_create(entity)
        return entity

    async def update(self, entity: RedisSortedSet, *args, **kwargs) -> RedisSortedSet:
        entity, _ = await self.update_or_create(entity)
        return entity

    async def delete(self, key: str, *args, **kwargs) -> None:
        await self._client.zrem(self.key_name, member=key)

    async def delete_by(self, conditions: Dict[str, Any], *args, **kwargs) -> None:
        await self._client.zrem(
            self.key_name,
            *[
                getattr(entity, self.key_field)
                for entity in await self.find_by(conditions)
            ]
        )

    async def delete_all(self, *args, **kwargs) -> None:
        await self._client.delete(self.key_name)

    async def get_or_create(
        self, entity: RedisSortedSet, *args, **kwargs
    ) -> Tuple[RedisSortedSet, bool]:
        _entity: Optional[RedisSortedSet] = await self.find_by_key(
            getattr(entity, self.key_field)
        )
        created: bool = False
        if _entity is None:
            _entity, created = await self.update_or_create(entity)
        return _entity, created

    async def update_or_create(
        self, entity: RedisSortedSet, ignore_expire: bool = False, *args, **kwargs
    ) -> Tuple[RedisSortedSet, bool]:
        pipe: Pipeline = self._client.pipeline()
        created = pipe.zadd(key=self.key_name, **entity.dict())
        if not ignore_expire and self.timeout > 0:
            pipe.expire(self.key_name, self.timeout)
        await pipe.execute()
        return entity, bool(await created)

    async def bulk_create(
        self, entities: List[RedisSortedSet], *args, **kwargs
    ) -> List[RedisSortedSet]:
        return await self.bulk_update(entities)

    async def bulk_update(
        self, entities: List[RedisSortedSet], *args, **kwargs
    ) -> List[RedisSortedSet]:
        _entities: List[RedisSortedSet] = []
        for entity in entities:
            _entities.append(await self.update_or_create(entity, ignore_expire=True))
        if self.timeout > 0:
            self._client.expire(key=self.key_name, timeout=self.timeout)

        return entities

    async def rank(self, key: str, *args, **kwargs) -> Optional[int]:
        return await self._client.zrank(self.key_name, key)

    async def incr(
        self, increment: int, key: str, ignore_expire: bool = False, *args, **kwargs
    ) -> RedisSortedSet:
        pipe: Pipeline = self._client.pipeline()
        score = pipe.zincrby(self.key_name, increment=increment, member=key)
        if not ignore_expire and self.timeout > 0:
            pipe.expire(self.key_name, self.timeout)
        await pipe.execute()
        return self.entity_cls.parse_obj({"member": key, "score": int(await score)})

    async def bulk_incr(
        self, increment: int, keys: List[str], *args, **kwargs
    ) -> List[RedisSortedSet]:
        entities: List[RedisSortedSet] = []
        for key in keys:
            entities.append(
                await self.incr(increment=increment, key=key, ignore_expire=True)
            )

        if self.timeout > 0:
            await self._client.expire(self.key_name, self.timeout)

        return entities
