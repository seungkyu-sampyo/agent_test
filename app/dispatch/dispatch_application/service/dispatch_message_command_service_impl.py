from uuid6 import UUID

from app.dispatch.dispatch_core import (
    DispatchMessageCommandService,
    DispatchMessage,
    DispatchMessageUow,
)


class DispatchMessageCommandServiceImpl(DispatchMessageCommandService):

    def __init__(self, message_uow: DispatchMessageUow):
        self._message_uow = message_uow

    async def create_message(
        self, thread_id: UUID, role: str, content: str
    ) -> DispatchMessage:
        message = DispatchMessage(
            thread_id=thread_id,
            role=role,
            content=content,
        )
        async with self._message_uow as uow:
            await uow.dispatch_message_repository.save(dispatch_message=message)

        return message
