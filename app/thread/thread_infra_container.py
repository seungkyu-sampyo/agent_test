from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from .thread_core import ThreadRepository
from .thread_infra import ThreadRepositoryDB
from .thread_infra.uow.thread_uow_impl import ThreadUowImpl


def get_thread_repository(
    session: AsyncSession = Depends(get_session),
) -> ThreadRepository:
    return ThreadRepositoryDB(session=session)


def get_thread_uow(session: AsyncSession = Depends(get_session)) -> ThreadUowImpl:
    return ThreadUowImpl(
        session=session, thread_repository_factory=get_thread_repository
    )
