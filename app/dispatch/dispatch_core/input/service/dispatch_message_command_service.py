from abc import ABC, abstractmethod
from uuid6 import UUID

from ...dispatch_message import DispatchMessage


class DispatchMessageCommandService(ABC):

    @abstractmethod
    async def create_message(
        self, thread_id: UUID, role: str, content: str
    ) -> DispatchMessage: ...
