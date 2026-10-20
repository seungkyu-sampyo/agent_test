from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid6 import UUID

from app.dispatch.dispatch_core import (
    DispatchMessageRepository,
    DispatchMessage,
)
from ..entity.dispatch_message_entity import DispatchMessageEntity
from ..mapper import dispatch_message_mapper


class DispatchMessageRepositoryDB(DispatchMessageRepository):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_id(self, message_id: UUID) -> Optional[DispatchMessage]:
        stmt = select(DispatchMessageEntity).where(
            DispatchMessageEntity.id_ == str(message_id)
        )
        result = await self._session.execute(stmt)
        entity: DispatchMessageEntity | None = result.scalar_one_or_none()

        if entity is None:
            return None

        return dispatch_message_mapper.to_domain(entity=entity)

    async def find_by_thread_id(self, thread_id: UUID) -> list[DispatchMessage]:
        stmt = (
            select(DispatchMessageEntity)
            .where(DispatchMessageEntity.thread_id == str(thread_id))
            .order_by(DispatchMessageEntity.created_at.asc())
        )
        result = await self._session.execute(stmt)
        entities = result.scalars().all()

        return [dispatch_message_mapper.to_domain(e) for e in entities]

    async def save(self, dispatch_message: DispatchMessage) -> DispatchMessage:
        entity = dispatch_message_mapper.to_entity(dispatch_message)
        self._session.add(entity)
        return dispatch_message
