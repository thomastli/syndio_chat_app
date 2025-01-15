import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch

from flask import Flask
from pymongo.collection import Collection
from pymongo.results import InsertOneResult, DeleteResult

from config.constants import Constants, EnvironmentVariables
from db.mongo_db import MongoDb
from models.message import Message

@pytest.fixture
def app():
    """Create a Flask test app"""
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def mock_mongo(app):
    """Create a mock MongoDB instance"""
    with patch('db.mongo_db.PyMongo') as mock_pymongo:
        mock_collection = MagicMock(spec=Collection)

        mock_instance = mock_pymongo.return_value
        mock_instance.db.messages = mock_collection
        
        # Initialize MongoDb with our mocked PyMongo
        db = MongoDb(app)
        
        return db, mock_collection

def test_insert_message_success(mock_mongo):
    """Test successful message insertion"""
    db, mock_collection = mock_mongo

    test_message = Message(
        user="test_user",
        message="test message",
        timestamp=datetime.now()
    )

    mock_collection.insert_one.return_value = InsertOneResult(
        inserted_id='test_id',
        acknowledged=True
    )

    result = db.insert_message(test_message)

    assert result is True
    mock_collection.insert_one.assert_called_once_with(dict(test_message))

def test_insert_message_failure(mock_mongo):
    """Test failed message insertion"""
    db, mock_collection = mock_mongo

    test_message = Message(
        user="test_user",
        message="test message",
        timestamp=datetime.now()
    )

    # Setup mock return value for failure
    mock_collection.insert_one.return_value = InsertOneResult(
        inserted_id='test_id',
        acknowledged=False
    )

    result = db.insert_message(test_message)
    assert result is False
    mock_collection.insert_one.assert_called_once_with(dict(test_message))

def test_retrieve_messages_empty(mock_mongo):
    """Test retrieving messages when none exist"""
    db, mock_collection = mock_mongo
    
    # Setup mock return value
    mock_collection.find.return_value = []

    messages = db.retrieve_messages()

    assert messages == []
    mock_collection.find.assert_called_once_with()

def test_retrieve_messages_with_data(mock_mongo):
    """Test retrieving messages when messages exist"""
    db, mock_collection = mock_mongo

    test_messages = [
        {
            Constants.USER_FIELD: "user1",
            Constants.MESSAGE_FIELD: "message1",
            Constants.TIMESTAMP_FIELD: datetime.now()
        },
        {
            Constants.USER_FIELD: "user2",
            Constants.MESSAGE_FIELD: "message2",
            Constants.TIMESTAMP_FIELD: datetime.now()
        }
    ]
    
    # Setup mock return value
    mock_collection.find.return_value = test_messages

    messages = db.retrieve_messages()

    assert messages == test_messages
    assert len(messages) == 2
    mock_collection.find.assert_called_once_with()

def test_clear_messages(mock_mongo):
    """Test clearing all messages"""
    db, mock_collection = mock_mongo

    db.clear_messages()

    mock_collection.drop.assert_called_once_with()

@pytest.mark.integration
def test_mongodb_integration(app):
    """Integration test with real MongoDB (mark this test to run only when needed)"""
    import os
    
    # Skip if no MongoDB URI is provided
    mongodb_uri = os.getenv(EnvironmentVariables.MONGO_URI_VARIABLE)
    if not mongodb_uri:
        pytest.skip("No MONGO_URI environment variable found")
    
    # Initialize real MongoDB connection
    app.config["MONGO_URI"] = mongodb_uri
    db = MongoDb(app)
    
    # Clear any existing messages
    db.clear_messages()
    
    # Test message
    test_message = Message(
        user="integration_test_user",
        message="integration test message",
        timestamp=datetime.now()
    )
    
    # Test insert
    insert_result = db.insert_message(test_message)
    assert insert_result is True
    
    # Test retrieve
    messages = db.retrieve_messages()
    assert len(messages) == 1
    assert messages[0][Constants.USER_FIELD] == "integration_test_user"
    assert messages[0][Constants.MESSAGE_FIELD] == "integration test message"
    
    # Test clear
    db.clear_messages()
    messages = db.retrieve_messages()
    assert len(messages) == 0
