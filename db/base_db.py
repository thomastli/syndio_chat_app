from abc import ABC, abstractmethod

from models.message import Message


class BaseDb(ABC):
    @abstractmethod
    def insert_message(self, message: Message) -> bool: # pragma: no cover
        pass

    @abstractmethod
    def retrieve_messages(self) -> list: # pragma: no cover
        pass

    @abstractmethod
    def clear_messages(self): # pragma: no cover
        pass