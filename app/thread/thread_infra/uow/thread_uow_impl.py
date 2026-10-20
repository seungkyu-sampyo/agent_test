from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from ...thread_core import ThreadUow, ThreadRepository


class ThreadUowImpl(ThreadUow):
    def __init__(
        self,
        session: AsyncSession,
        thread_repository_factory: Callable[[AsyncSession], ThreadRepository],
    ):
        self.session = session
        self.thread_repository = thread_repository_factory(session)

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
