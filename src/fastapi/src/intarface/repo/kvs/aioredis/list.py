from typing import Any, Callable, Dict, List, Optional, Tuple

from aioredis.commands.transaction import Pipeline
from pydantic import BaseModel

from intarface.repo import IAioDataStoreRepo

from .core import AioRedisRepo


class AioRedisListRepo(IAioDataStoreRepo, AioRedisRepo):
    async def find_all(
        self, order: Optional[List[str]] = None, count: int = -1, *args, **kwargs
    ) -> List[BaseModel]:
        entities: List[BaseModel] = [
            self.entity_cls.parse_raw(json_str)
            for json_str in await self._client.lrange(self.key_name, 0, count)
        ]
        if order is not None:
            entities = self._order_by(entities, order)
        return entities

    async def find_by(
        self,
        conditions: Dict[str, Any],
        order: Optional[List[str]] = None,
        count: int = -1,
        *args,
        **kwargs
    ) -> List[BaseModel]:
        entities: List[BaseModel] = await self.find_all(order=order, count=count)
        if len(entities) > 0:
            for key, val in conditions.items():
                entities = [e for e in entities if getattr(e, key) == val]
        return entities

    async def count_by(
        self, conditions: Optional[Dict[str, str]] = None, *args, **kwargs
    ) -> int:
        if conditions is None:
            return await self._client.llen(self.key_name)
        else:
            return len(await self.find_by(conditions))

    async def find_by_key(self, key: str, *args, **kwargs) -> List[BaseModel]:
        return await self.find_by(conditions={self.key_field: key})

    async def find_by_index(self, index: int, *args, **kwargs) -> Optional[BaseModel]:
        json_str: str = await self._client.lindex(key=self.key_name, index=index)
        if json_str is None:
            return None
        return self.entity_cls.parse_raw(json_str)

    async def create(
        self,
        entity: BaseModel,
        left: bool = True,
        pivot: Optional[BaseModel] = None,
        pipe: Optional[Pipeline] = None,
        *args,
        **kwargs
    ) -> BaseModel:
        _pipe: Pipeline = self._client.pipeline() if pipe is None else pipe
        if pivot is None:
            push: Callable = _pipe.lpush if left else _pipe.rpush
            push(key=self.key_name, value=entity.json())
        else:
            _pipe.linsert(
                key=self.key_name,
                pivot=pivot.json(),
                value=entity.json(),
                before=left,
            )

        if pipe is None:
            if self.timeout > 0:
                _pipe.expire(self.key_name, self.timeout)
            await _pipe.execute()
        return entity

    async def find_index(
        self, entity: BaseModel, entities: Optional[List[BaseModel]] = None
    ) -> List[int]:
        _entities: List[BaseModel] = (
            await self.find_all() if entities is None else entities
        )
        indexes: List[int] = [
            i
            for i, e in enumerate(_entities)
            if getattr(e, self.key_field) == getattr(entity, self.key_field)
        ]
        return indexes

    async def update_by_index(
        self, entity: BaseModel, index: int, *args, **kwargs
    ) -> BaseModel:
        await self._client.lset(key=self.key_name, index=index, value=entity.json())
        return entity

    async def update(
        self,
        entity: BaseModel,
        entities: Optional[List[BaseModel]] = None,
        pipe: Optional[Pipeline] = None,
        *args,
        **kwargs
    ) -> BaseModel:
        indexes = await self.find_index(entity=entity, entities=entities)

        _pipe: Pipeline = self._client.pipeline() if pipe is None else pipe
        for i in indexes:
            _pipe.lset(key=self.key_name, index=i, value=entity.json())

        if pipe is None:
            if self.timeout > 0:
                _pipe.expire(self.key_name, self.timeout)
            await _pipe.execute()
        return entity

    async def delete(self, key: str, *args, **kwargs) -> None:
        pipe: Pipeline = self._client.pipeline()
        for e in await self.find_by_key(key):
            pipe.lrem(key=self.key_name, count=1, value=e.json())
        await pipe.execute()

    async def delete_by(self, conditions: Dict[str, Any], *args, **kwargs) -> None:
        pipe: Pipeline = self._client.pipeline()
        for e in await self.find_by(conditions):
            pipe.lrem(key=self.key_name, count=1, value=e.json())
        await pipe.execute()

    async def delete_all(self, *args, **kwargs) -> None:
        await self._client.delete(self.key_name)

    async def get_or_create(
        self,
        entity: BaseModel,
        left: bool = True,
        pivot: Optional[BaseModel] = None,
        *args,
        **kwargs
    ) -> Tuple[List[BaseModel], bool]:
        entities: List[BaseModel] = await self.find_by_key(
            getattr(entity, self.key_field)
        )
        created: bool = False

        if len(entities) == 0:
            entities = [await self.create(entity=entity, left=left, pivot=pivot)]
            created = True
        return entities, created

    async def update_or_create(
        self,
        entity: BaseModel,
        left: bool = True,
        pivot: Optional[BaseModel] = None,
        entities: Optional[List[BaseModel]] = None,
        *args,
        **kwargs
    ) -> Tuple[BaseModel, bool]:
        indexes = await self.find_index(entity=entity, entities=entities)
        created: bool = False

        if len(indexes) == 0:
            entity = await self.create(entity=entity, left=left, pivot=pivot)
            created = True
        else:
            pipe: Pipeline = self._client.pipeline()
            for i in indexes:
                pipe.lset(key=self.key_name, index=i, value=entity.json())

            pipe.expire(self.key_name, self.timeout)
            await pipe.execute()

        return entity, created

    async def bulk_create(
        self,
        entities: List[BaseModel],
        left: bool = True,
        pivot: Optional[BaseModel] = None,
        *args,
        **kwargs
    ) -> List[BaseModel]:
        pipe: Pipeline = self._client.pipeline()
        for e in entities:
            await self.create(entity=e, left=left, pivot=pivot, pipe=pipe)

        pipe.expire(self.key_name, self.timeout)
        await pipe.execute()
        return entities

    async def bulk_update(
        self, entities: List[BaseModel], *args, **kwargs
    ) -> List[BaseModel]:
        pipe: Pipeline = self._client.pipeline()
        _entities: List[BaseModel] = [
            await self.update(entity=e, entities=await self.find_all(), pipe=pipe)
            for e in entities
        ]

        pipe.expire(self.key_name, self.timeout)
        await pipe.execute()
        return _entities

    async def pop(
        self, right: bool = True, blocking: bool = False, timeout: int = 60
    ) -> Optional[BaseModel]:
        entity: Optional[BaseModel] = None
        json_str: Optional[str] = None
        pop: Callable
        if blocking:
            pop = self._client.brpop if right else self._client.blpop
            json_str = await pop(key=self.key_name, timeout=timeout)
        else:
            pop = self._client.rpop if right else self._client.lpop
            json_str = await pop(self.key_name)

        if json_str is not None:
            entity = self.entity_cls.parse_raw(json_str)
        return entity

    async def bulk_pop(self, count: int, right: bool = True) -> List[BaseModel]:
        pipe: Pipeline = self._client.pipeline()
        pop: Callable = pipe.rpop if right else pipe.lpop
        for i in range(0, count):
            pop(self.key_name)
        entities: List[BaseModel] = [
            self.entity_cls.parse_raw(json_str)
            for json_str in await pipe.execute()
            if json_str is not None
        ]
        return entities

    async def trim(self, start: int, stop: int) -> None:
        pipe: Pipeline = self._client.pipeline()
        pipe.ltrim(self.key_name, start, stop)
        pipe.expire(self.key_name, self.timeout)
        pipe.execute()

    async def rpoplpush(self, blocking: bool = False) -> None:
        raise NotImplementedError()
