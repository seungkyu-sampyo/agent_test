from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from app.dispatch.dispatch_core import DispatchMessageUow, DispatchMessageRepository


class DispatchMessageUowImpl(DispatchMessageUow):

    def __init__(
        self,
        session: AsyncSession,
        dispatch_message_repository_factory: Callable[
            [AsyncSession], DispatchMessageRepository
        ],
    ):
        self.session = session
        self.dispatch_message_repository = dispatch_message_repository_factory(session)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
