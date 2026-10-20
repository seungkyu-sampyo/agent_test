from abc import ABC, abstractmethod


class ThreadQueryService(ABC):

    @abstractmethod
    def retrieve_thread(self, _id: str): ...
