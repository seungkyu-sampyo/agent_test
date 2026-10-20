from uuid6 import UUID

from app.thread.thread_core import ThreadQueryService, Thread, ThreadRepository


class ThreadQueryServiceImpl(ThreadQueryService):

    def __init__(
        self,
        thread_repository: ThreadRepository,
    ):
        self._thread_repository = thread_repository

    async def retrieve_thread(self, thread_id: UUID) -> Thread:

        thread: Thread | None = await self._thread_repository.find_by_id(
            thread_id=thread_id
        )

        if thread is None:
            raise ValueError()

        return thread
