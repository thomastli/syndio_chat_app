import os

from dotenv import load_dotenv
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
        result = self.db.messages.insert_one(dict(message))
        return result.acknowledged

    def retrieve_messages(self) -> list:
        messages = list(self.db.messages.find())
        return messages

    def clear_messages(self):
        self.db.messages.drop()