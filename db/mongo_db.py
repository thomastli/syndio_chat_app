from flask import Flask
from flask_pymongo import PyMongo

from db.base_db import BaseDb
from models.message import Message



class MongoDb(BaseDb):
    def __init__(self, app: Flask):
        self.app = app
        self.mongo = PyMongo(app)
        self.db = self.mongo.db

    def insert_message(self, message: Message) -> bool:
        """ Insert a message into the database.

        :param:
            message: The message to be inserted.

        :return:
            Whether the insertion was successful.
        """
        result = self.db.messages.insert_one(dict(message))
        return result.acknowledged

    def retrieve_messages(self) -> list:
        """ Retrieves all messages from the database.

        :return:
            A list of messages retrieved.
        """
        messages = list(self.db.messages.find())
        return messages

    def clear_messages(self):
        """ Clears all messages from the database."""
        self.db.messages.drop()