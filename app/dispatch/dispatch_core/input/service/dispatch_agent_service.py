from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Any


@dataclass
class DispatchChatResult:
    reply: str
    thread_id: Optional[str] = None
    data: Optional[Any] = None


class DispatchAgentService(ABC):

    @abstractmethod
    async def chat(
        self, message: str, thread_id: Optional[str] = None
    ) -> DispatchChatResult: ...
