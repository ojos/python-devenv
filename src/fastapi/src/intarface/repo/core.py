from abc import ABCMeta, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel


class IAioDataStoreRepo(metaclass=ABCMeta):
    @abstractmethod
    async def find_all(
        self,
        order: Optional[List[str]] = None,
        count: Optional[int] = None,
        *args,
        **kwargs
    ) -> List[BaseModel]:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "find_all")
        )

    @abstractmethod
    async def find_by(
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

    @abstractmethod
    async def count_by(
        self, conditions: Optional[Dict[str, str]] = None, *args, **kwargs
    ) -> int:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "count_by")
        )

    @abstractmethod
    async def find_by_key(self, key: str, *args, **kwargs) -> Optional[BaseModel]:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "find_by_key")
        )

    @abstractmethod
    async def create(self, entity: BaseModel, *args, **kwargs) -> BaseModel:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "create")
        )

    @abstractmethod
    async def update(self, entity: BaseModel, *args, **kwargs) -> None:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "uodate")
        )

    @abstractmethod
    async def delete(self, key: str, *args, **kwargs) -> None:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "delete")
        )

    @abstractmethod
    async def delete_by(
        self, conditions: Optional[Dict[str, Any]] = None, *args, **kwargs
    ) -> None:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "delete_by")
        )

    @abstractmethod
    async def delete_all(self, *args, **kwargs) -> None:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "delete_all")
        )

    @abstractmethod
    async def get_or_create(
        self, entity: BaseModel, *args, **kwargs
    ) -> Tuple[BaseModel, bool]:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "get_or_create")
        )

    @abstractmethod
    async def update_or_create(
        self, entity: BaseModel, *args, **kwargs
    ) -> Tuple[BaseModel, bool]:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "update_or_create")
        )

    @abstractmethod
    async def bulk_create(
        self, entities: List[BaseModel], *args, **kwargs
    ) -> List[BaseModel]:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "bulk_create")
        )

    @abstractmethod
    async def bulk_update(self, entities: List[BaseModel], *args, **kwargs) -> None:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "bulk_updateS")
        )


class IDataStoreRepo(metaclass=ABCMeta):
    @abstractmethod
    def find_all(
        self,
        order: Optional[List[str]] = None,
        count: Optional[int] = None,
        *args,
        **kwargs
    ) -> List[BaseModel]:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "find_all")
        )

    @abstractmethod
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

    @abstractmethod
    def count_by(
        self, conditions: Optional[Dict[str, str]] = None, *args, **kwargs
    ) -> int:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "count_by")
        )

    @abstractmethod
    def find_by_key(self, key: str, *args, **kwargs) -> Optional[BaseModel]:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "find_by_key")
        )

    @abstractmethod
    def create(self, entity: BaseModel, *args, **kwargs) -> BaseModel:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "create")
        )

    @abstractmethod
    def update(self, entity: BaseModel, *args, **kwargs) -> None:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "uodate")
        )

    @abstractmethod
    def delete(self, key: str, *args, **kwargs) -> None:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "delete")
        )

    @abstractmethod
    def delete_by(
        self, conditions: Optional[Dict[str, Any]] = None, *args, **kwargs
    ) -> None:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "delete_by")
        )

    @abstractmethod
    def delete_all(self, *args, **kwargs) -> None:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "delete_all")
        )

    @abstractmethod
    def get_or_create(
        self, entity: BaseModel, *args, **kwargs
    ) -> Tuple[BaseModel, bool]:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "get_or_create")
        )

    @abstractmethod
    def update_or_create(
        self, entity: BaseModel, *args, **kwargs
    ) -> Tuple[BaseModel, bool]:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "update_or_create")
        )

    @abstractmethod
    def bulk_create(
        self, entities: List[BaseModel], *args, **kwargs
    ) -> List[BaseModel]:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "bulk_create")
        )

    @abstractmethod
    def bulk_update(self, entities: List[BaseModel], *args, **kwargs) -> None:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "bulk_updateS")
        )
