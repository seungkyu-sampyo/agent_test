from abc import ABC, abstractmethod
from typing import Optional

from app.thread.thread_core import Thread


class ThreadRepository(ABC):

    @abstractmethod
    async def find_by_id(self, thread_id: str) -> Optional[Thread]: ...

    @abstractmethod
    async def save(self, thread: Thread) -> Thread: ...
