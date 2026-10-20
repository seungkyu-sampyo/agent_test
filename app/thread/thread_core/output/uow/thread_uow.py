from abc import ABC, abstractmethod

from ..repository.thread_repository import ThreadRepository


class ThreadUow(ABC):
    thread_repository: ThreadRepository

    @abstractmethod
    async def __aenter__(self) -> "ThreadUow": ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...
