from ...thread_core import ThreadCommandService, Thread, ThreadUow


class ThreadCommandServiceImpl(ThreadCommandService):
    def __init__(
        self,
        thread_uow: ThreadUow,
    ):
        self._thread_uow: ThreadUow = thread_uow

    async def create_thread(self) -> Thread:
        thread: Thread = Thread()

        async with self._thread_uow as uow:
            await uow.thread_repository.save(thread=thread)

        return thread
