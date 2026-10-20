from abc import ABC, abstractmethod
from typing import Optional
from uuid6 import UUID

from ...dispatch_message import DispatchMessage


class DispatchMessageQueryService(ABC):

    @abstractmethod
    async def get_message_by_id(
        self, message_id: UUID
    ) -> Optional[DispatchMessage]: ...

    @abstractmethod
    async def get_messages_by_thread_id(
        self, thread_id: UUID
    ) -> list[DispatchMessage]: ...
