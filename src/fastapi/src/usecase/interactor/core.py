from abc import ABCMeta, abstractmethod
from typing import Any


class IInteractor(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "execute")
        )


class IAioInteractor(metaclass=ABCMeta):
    @abstractmethod
    async def execute(self, *args, **kwargs) -> Any:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "execute")
        )
