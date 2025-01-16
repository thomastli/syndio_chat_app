from datetime import datetime

from flask import Flask
from flask_pymongo import PyMongo

from config.constants import Constants
from db.base_db import BaseDb
from models.message import Message


class MongoDb(BaseDb):
    """Class that defines a wrapper for a MongoDB instance"""

    def __init__(self, app: Flask):
        """Initializes a MongoDB instance

        Args:
            app:   The Flask application

        Returns:
            A MongoDB object
        """
        self.app = app
        self.mongo = PyMongo(app)
        self.db = self.mongo.db

    def insert_message(self, message: Message) -> bool:
        """Insert a message into the database.

        Args:
            message: The message to be inserted.

        Returns:
            Whether the insertion was successful.
        """
        result = self.db.messages.insert_one(dict(message))
        return result.acknowledged

    def retrieve_messages(self) -> list[dict]:
        """Retrieves all messages from the database.

        Returns:
            A list of messages retrieved.
        """
        messages = list(self.db.messages.find())
        return messages

    def clear_messages(self):
        """Clears all messages from the database."""
        self.db.messages.drop()

    def count_messages(self) -> int:
        """Counts the number of messages in the database.

        Returns:
            The number of messages
        """
        return self.db.messages.count_documents({})

    def get_nth_newest(self) -> list[dict]:
        """Get the nth newest message in the database.

        Returns:
            The nth newest message
        """
        docs = self.db.messages.find().sort(Constants.TIMESTAMP_FIELD, -1).skip(
            self.app.config[Constants.MAX_MESSAGES_FIELD]).limit(1)

        return list(docs)

    def delete_messages_by_timestamp(self, timestamp: datetime):
        """Delete all messages from the database before a given cutoff timestamp.

        Args:
            timestamp: The cutoff timestamp
        """
        self.db.messages.delete_many({Constants.TIMESTAMP_FIELD: {"$lte": timestamp}})
