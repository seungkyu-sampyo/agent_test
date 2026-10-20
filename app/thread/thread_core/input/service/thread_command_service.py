from abc import ABC, abstractmethod


class ThreadCommandService(ABC):

    @abstractmethod
    def create_thread(self): ...
