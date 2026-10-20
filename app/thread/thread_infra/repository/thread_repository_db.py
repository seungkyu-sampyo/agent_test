from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid6 import UUID

from app.thread.thread_core import Thread
from app.thread.thread_core.output.repository.thread_repository import ThreadRepository
from ..entity.thread_entity import ThreadEntity
from ..mapper import thread_mapper


class ThreadRepositoryDB(ThreadRepository):

    def __init__(self, session: AsyncSession):

        self._session = session

    async def find_by_id(self, thread_id: UUID) -> Optional[Thread]:
        stmt = select(ThreadEntity).where(
            ThreadEntity.id_ == thread_id, ThreadEntity.deleted_at.is_(None)
        )

        result = await self._session.execute(stmt)
        thread_entity: ThreadEntity | None = result.scalar_one_or_none()

        if thread_entity is None:
            return None

        return thread_mapper.to_domain(thread_entity=thread_entity)

    async def save(self, thread: Thread) -> Thread:
        thread_entity = thread_mapper.to_entity(thread)

        self._session.add(thread_entity)

        return thread
