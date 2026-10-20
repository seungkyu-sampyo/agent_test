from fastapi import Depends

from .thread_core import (
    ThreadQueryService,
    ThreadCommandService,
    ThreadRepository,
    ThreadUow,
)
from .thread_application import ThreadQueryServiceImpl, ThreadCommandServiceImpl
from .thread_infra_container import get_thread_repository, get_thread_uow


def get_thread_query_service(
    thread_repository: ThreadRepository = Depends(get_thread_repository),
) -> ThreadQueryService:
    return ThreadQueryServiceImpl(thread_repository=thread_repository)


def get_thread_command_service(
    thread_uow: ThreadUow = Depends(get_thread_uow),
) -> ThreadCommandService:
    return ThreadCommandServiceImpl(thread_uow=thread_uow)
