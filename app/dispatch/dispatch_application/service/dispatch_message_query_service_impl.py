from typing import Optional
from uuid6 import UUID

from app.dispatch.dispatch_core import (
    DispatchMessageQueryService,
    DispatchMessage,
    DispatchMessageRepository,
)


class DispatchMessageQueryServiceImpl(DispatchMessageQueryService):

    def __init__(self, message_repository: DispatchMessageRepository):
        self._message_repository = message_repository

    async def get_message_by_id(self, message_id: UUID) -> Optional[DispatchMessage]:
        return await self._message_repository.find_by_id(message_id)

    async def get_messages_by_thread_id(
        self, thread_id: UUID
    ) -> list[DispatchMessage]:
        return await self._message_repository.find_by_thread_id(thread_id)
