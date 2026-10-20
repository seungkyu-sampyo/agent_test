from abc import ABC, abstractmethod

from ..repository.re_mi_con_dispatch_repository import ReMiConDispatchRepository


class ReMiConDispatchUow(ABC):
    re_mi_con_dispatch_repository: ReMiConDispatchRepository

    @abstractmethod
    async def __aenter__(self) -> "ReMiConDispatchUow": ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...
