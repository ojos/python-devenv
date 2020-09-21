from typing import Any, Dict, Iterable, List, Optional, Tuple, cast

from aioredis.commands.transaction import Pipeline
from pydantic import BaseModel

from intarface.repo import IAioDataStoreRepo

from .core import AioRedisRepo


class AioRedisStringRepo(IAioDataStoreRepo, AioRedisRepo):
    async def _find_all_keys(self) -> List[str]:
        return await self._client.keys(pattern=self.key_name.format("*"))

    async def find_all(
        self,
        order: Optional[List[str]] = None,
        count: Optional[int] = None,
        *args,
        **kwargs
    ) -> List[BaseModel]:
        all_keys: List[str] = await self._find_all_keys()
        if len(all_keys) > 0:
            entities: List[BaseModel] = [
                self.entity_cls.parse_raw(json_str)
                for json_str in cast(
                    Iterable[str], filter(None, await self._client.mget(*all_keys))
                )
            ]
            if order is not None:
                entities = self._order_by(entities, order)
            if count is not None:
                entities = entities[:count]
        else:
            entities = []
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
            return len(await self.find_all())
        else:
            return len(await self.find_by(conditions))

    async def find_by_key(self, key: str, *args, **kwargs) -> Optional[BaseModel]:
        json_str: str = await self._client.get(key=self.key_name.format(key))
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
        await self._client.delete(self.key_name.format(key))

    async def delete_by(self, conditions: Dict[str, Any], *args, **kwargs) -> None:
        await self._client.delete(
            *[
                self.key_name.format(getattr(entity, self.key_field))
                for entity in await self.find_by(conditions)
            ]
        )

    async def delete_all(self, *args, **kwargs) -> None:
        await self._client.delete(
            *[
                self.key_name.format(getattr(entity, self.key_field))
                for entity in await self.find_all()
            ]
        )

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
        key_name: str = self.key_name.format(getattr(entity, self.key_field))
        created: int = await self._client.set(
            key=key_name, value=json_str, expire=self.timeout
        )
        return entity, bool(created)

    async def bulk_create(
        self, entities: List[BaseModel], *args, **kwargs
    ) -> List[BaseModel]:
        return await self.bulk_update(entities)

    async def bulk_update(
        self, entities: List[BaseModel], *args, **kwargs
    ) -> List[BaseModel]:
        json_dicts = {
            self.key_name.format(getattr(entity, self.key_field)): entity.json()
            for entity in entities
        }
        pipe: Pipeline = self._client.pipeline()
        pipe.mset(json_dicts)

        if self.timeout > 0:
            for key in json_dicts.keys():
                pipe.expire(key=key, timeout=self.timeout)
        await pipe.execute()

        return entities
