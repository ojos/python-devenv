from typing import Any, Dict, List, Optional, Tuple, Type

from aioredis import ConnectionsPool
from aioredis.commands.transaction import Pipeline
from pydantic import BaseModel

from intarface.repo import IAioDataStoreRepo

from .core import AioRedisRepo


class AioRedisHashRepo(IAioDataStoreRepo, AioRedisRepo):
    def __init__(
        self,
        client: ConnectionsPool,
        key_name: str = "app/key_name",
        entity_cls: Type[BaseModel] = BaseModel,
        timeout: int = 60 * 3,
        key_field: str = "id",
        *args,
        **kwargs
    ):
        super(AioRedisHashRepo, self).__init__(
            client, key_name, entity_cls, timeout, *args, **kwargs
        )
        self._key_field = key_field

    @property
    def key_field(self) -> str:
        return self._key_field

    async def find_all(
        self,
        order: Optional[List[str]] = None,
        count: Optional[int] = None,
        *args,
        **kwargs
    ) -> List[BaseModel]:
        entities = [
            self.entity_cls.parse_raw(json_str)
            for json_str in await self._client.hgetall(self.key_name).values()
        ]
        if order is not None:
            entities = self._order_by(entities, order)
        if count is not None:
            entities = entities[:count]
        return entities

    async def find_by(
        self,
        conditions: Dict[str, Any],
        order: Optional[List[str]] = None,
        count: Optional[int] = None,
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
            return await self._client.hlen(self.key_name)
        else:
            return len(await self.find_by(conditions))

    async def find_by_key(self, key: str, *args, **kwargs) -> Optional[BaseModel]:
        json_str: str = await self._client.hget(key=self.key_name, field=key)
        if json_str is None:
            return None
        return self.entity_cls.parse_raw(json_str)

    async def create(self, entity: BaseModel, *args, **kwargs) -> BaseModel:
        entity, _ = await self.update_or_create(entity)
        return entity

    async def update(self, entity: BaseModel, *args, **kwargs) -> BaseModel:
        entity, _ = await self.update_or_create(entity)
        return entity

    async def delete(self, key: str, *args, **kwargs) -> None:
        await self._client.hdel(self.key_name, field=key)

    async def delete_by(self, conditions: Dict[str, Any], *args, **kwargs) -> None:
        await self._client.hdel(
            self.key_name,
            *[
                getattr(entity, self.key_field)
                for entity in await self.find_by(conditions)
            ]
        )

    async def delete_all(self, *args, **kwargs) -> None:
        await self._client.delete(self.key_name)

    async def get_or_create(
        self, entity: BaseModel, *args, **kwargs
    ) -> Tuple[BaseModel, bool]:
        _entity: Optional[BaseModel] = await self.find_by_key(
            getattr(entity, self.key_field)
        )
        created: bool = False
        if _entity is None:
            _entity, created = await self.update_or_create(entity)
        return _entity, created

    async def update_or_create(
        self, entity: BaseModel, *args, **kwargs
    ) -> Tuple[BaseModel, bool]:
        json_str: str = entity.json()
        field: str = getattr(entity, self.key_field)

        created: int = await self._client.hset(
            key=self.key_name, field=field, value=json_str
        )
        if self.timeout > 0:
            await self._client.expire(self.key_name, self.timeout)
        return entity, bool(created)

    async def bulk_create(
        self, entities: List[BaseModel], *args, **kwargs
    ) -> List[BaseModel]:
        return await self.bulk_update(entities)

    async def bulk_update(
        self, entities: List[BaseModel], *args, **kwargs
    ) -> List[BaseModel]:
        json_dicts = {
            getattr(entity, self.key_field): entity.json() for entity in entities
        }
        pipe: Pipeline = self._client.pipeline()
        pipe.hmset(key=self.key_name, mapping=json_dicts)

        if self.timeout > 0:
            pipe.expire(self.key_name, self.timeout)
        await pipe.execute()

        return entities
