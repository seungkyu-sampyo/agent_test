from abc import ABC, abstractmethod

from ..repository.dispatch_message_repository import DispatchMessageRepository


class DispatchMessageUow(ABC):
    dispatch_message_repository: DispatchMessageRepository

    @abstractmethod
    async def __aenter__(self) -> "DispatchMessageUow": ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...
