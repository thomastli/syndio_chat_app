from abc import ABC, abstractmethod
from datetime import datetime

from models.message import Message


class BaseDb(ABC):
    @abstractmethod
    def insert_message(self, message: Message) -> bool: # pragma: no cover
        """Insert a message into the database.

        Args:
            message: The user message to be inserted

        Returns:
            Whether the insertion was successful
        """
        pass

    @abstractmethod
    def retrieve_messages(self) -> list: # pragma: no cover
        """ Retrieve all messages from the database.

        Returns:
            A list of messages
        """
        pass

    @abstractmethod
    def clear_messages(self): # pragma: no cover
        """Clear all messages from the database."""
        pass

    @abstractmethod
    def count_messages(self) -> int:
        """Counts the number of messages in the database.

        Returns:
            The number of messages
        """
        pass

    @abstractmethod
    def get_nth_newest(self) -> list:
        """Get the nth newest message in the database.

        Returns:
            The nth newest message
        """
        pass

    @abstractmethod
    def delete_messages_by_timestamp(self, timestamp: datetime):
        """Delete all messages from the database before a given cutoff timestamp.

        Args:
            timestamp: The cutoff timestamp
        """
        pass