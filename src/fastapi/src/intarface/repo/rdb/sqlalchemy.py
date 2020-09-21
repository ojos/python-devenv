from typing import Any, Dict, List, Optional, Tuple, Type

from pydantic import BaseModel

from intarface.repo import IDataStoreRepo
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.orm import Session
from usecase.serializer.core import ISerializer


class SqlalchemyRepo(object):
    def __init__(self, client: Session, serializer: Type[ISerializer], *args, **kwargs):
        self._client = client
        self._serializer = serializer

    @property
    def client(self) -> Session:
        return self._client

    @property
    def serializer(self) -> Type[ISerializer]:
        return self._serializer


class SqlalchemyOrmRepo(IDataStoreRepo, SqlalchemyRepo):
    def __init__(
        self,
        client: Session,
        serializer: Type[ISerializer],
        model_cls: Type[DeclarativeMeta],
        *args,
        **kwargs
    ):
        super(SqlalchemyOrmRepo, self).__init__(client, serializer)
        self._model_cls = model_cls

    @property
    def model_cls(self) -> Type[DeclarativeMeta]:
        return self._model_cls

    def find_all(
        self,
        order: Optional[List[str]] = None,
        count: Optional[int] = None,
        *args,
        **kwargs
    ) -> List[BaseModel]:
        # self.client.query(self.model_cls).all()
        pass

    def find_by(
        self,
        conditions: Dict[str, Any],
        order: Optional[List[str]] = None,
        count: Optional[int] = None,
        *args,
        **kwargs
    ) -> List[BaseModel]:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "find_by")
        )

    def count_by(
        self, conditions: Optional[Dict[str, str]] = None, *args, **kwargs
    ) -> int:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "count_by")
        )

    def find_by_key(self, key: str, *args, **kwargs) -> Optional[BaseModel]:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "find_by_key")
        )

    def create(self, entity: BaseModel, *args, **kwargs) -> BaseModel:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "create")
        )

    def update(self, entity: BaseModel, *args, **kwargs) -> None:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "uodate")
        )

    def delete(self, key: str, *args, **kwargs) -> None:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "delete")
        )

    def delete_by(
        self, conditions: Optional[Dict[str, Any]] = None, *args, **kwargs
    ) -> None:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "delete_by")
        )

    def delete_all(self, *args, **kwargs) -> None:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "delete_all")
        )

    def get_or_create(
        self, entity: BaseModel, *args, **kwargs
    ) -> Tuple[BaseModel, bool]:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "get_or_create")
        )

    def update_or_create(
        self, entity: BaseModel, *args, **kwargs
    ) -> Tuple[BaseModel, bool]:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "update_or_create")
        )

    def bulk_create(
        self, entities: List[BaseModel], *args, **kwargs
    ) -> List[BaseModel]:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "bulk_create")
        )

    def bulk_update(self, entities: List[BaseModel], *args, **kwargs) -> None:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "bulk_updateS")
        )
