from abc import ABC, abstractmethod


class ThreadCommandService(ABC):

    @abstractmethod
    async def create_thread(self): ...
