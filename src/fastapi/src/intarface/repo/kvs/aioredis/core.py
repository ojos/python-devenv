from operator import attrgetter
from typing import List, Type

from aioredis import ConnectionsPool
from pydantic import BaseModel


class AioRedisRepo(object):
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
        self._client = client
        self._key_name = key_name
        self._entity_cls = entity_cls
        self.timeout = timeout
        self._key_field = key_field

    @property
    def client(self) -> ConnectionsPool:
        return self._client

    @property
    def key_name(self) -> str:
        return self._key_name

    @property
    def entity_cls(self) -> Type[BaseModel]:
        return self._entity_cls

    @property
    def key_field(self) -> str:
        return self._key_field

    def _order_by(self, entities: List[BaseModel], order: List[str]) -> List[BaseModel]:
        _entities: List[BaseModel] = entities
        for key in order:
            if key[0] == "-":
                _entities = sorted(_entities, key=attrgetter(key[1:]), reverse=True)
            else:
                _entities = sorted(_entities, key=attrgetter(key))
        return _entities
