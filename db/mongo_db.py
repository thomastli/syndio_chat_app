import os

from flask import Flask
from flask_pymongo import PyMongo

from db.base_db import BaseDb
from models.message import Message


class MongoDb(BaseDb):
    def __init__(self, app: Flask):
        self.app = app
        self.app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/chat_app")
        self.mongo = PyMongo(app)

    def insert_message(self, message: Message) -> bool:
        result = self.mongo.db.messages.insert_one(dict(message))
        return result.acknowledged

    def retrieve_messages(self) -> list:
        messages = list(self.mongo.db.messages.find())
        return messages

    def clear_messages(self):
        self.mongo.db.messages.drop()