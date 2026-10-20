from abc import ABC, abstractmethod

from app.thread.thread_core import Thread


class ThreadRepository(ABC):

    @abstractmethod
    def find_by_id(self, _id: str): ...

    @abstractmethod
    def save(self, thread: Thread): ...
