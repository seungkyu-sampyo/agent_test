from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from ...dispatch_core import ReMiConDispatchUow, ReMiConDispatchRepository


class ReMiConDispatchUowImpl(ReMiConDispatchUow):
    def __init__(
        self,
        session: AsyncSession,
        re_mi_con_dispatch_repository_factory: Callable[
            [AsyncSession], ReMiConDispatchRepository
        ],
    ):
        self.session = session
        self.re_mi_con_dispatch_repository = re_mi_con_dispatch_repository_factory(
            session
        )

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
