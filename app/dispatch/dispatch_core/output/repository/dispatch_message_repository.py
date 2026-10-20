from uuid6 import UUID
from abc import ABC, abstractmethod
from typing import Optional

from ...dispatch_message import DispatchMessage


class DispatchMessageRepository(ABC):

    @abstractmethod
    async def find_by_id(self, message_id: UUID) -> Optional[DispatchMessage]: ...

    @abstractmethod
    async def find_by_thread_id(self, thread_id: UUID) -> list[DispatchMessage]: ...

    @abstractmethod
    async def save(self, dispatch_message: DispatchMessage) -> DispatchMessage: ...
