from app import app

import json
import pytest

from config.constants import StatusCodes, Constants


@pytest.fixture
def client():
    """Defines a Flask test client fixture"""
    app.config['TESTING'] = True
    app.config['MONGO_URI'] = 'mongodb://localhost:27017'

    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test that home page loads successfully"""
    response = client.get('/')
    assert response.status_code == StatusCodes.SUCCESS_CODE

def test_send_message(client):
    """Test sending a valid message"""
    response = client.post('/chat/message',
                         json={'message': 'Hello AI!'},
                         content_type='application/json')
    assert response.status_code == StatusCodes.SUCCESS_CODE

    data = json.loads(response.data)
    assert data[Constants.STATUS_FIELD] == 'success'

def test_send_invalid_message(client):
    """Test sending an invalid message"""
    response = client.post('/chat/message',
                         json={},
                         content_type='application/json')
    assert response.status_code == StatusCodes.BAD_REQUEST_ERROR_CODE

def test_get_history(client):
    """Test retrieving chat history"""
    # First, send a message
    client.post('/chat/message',
                json={'message': 'Test message'},
                content_type='application/json')
    
    # Then get history
    response = client.get('/chat/history')
    assert response.status_code == StatusCodes.SUCCESS_CODE

    data = json.loads(response.data)
    assert len(data) > 0
    assert isinstance(data, list)
    assert Constants.MESSAGE_FIELD in data[0]
    assert Constants.USER_FIELD in data[0]
    assert Constants.TIMESTAMP_FIELD in data[0]

def test_empty_message(client):
    """Test sending empty message"""
    response = client.post('/chat/message',
                         json={'message': '   '},
                         content_type='application/json')
    assert response.status_code == StatusCodes.BAD_REQUEST_ERROR_CODE

# def test_message_limit(client):
#     """Test that message limit is enforced"""
#     # Clear existing messages
#     db.clear_messages()
#
#     # Send more than MAX_MESSAGES messages
#     for i in range(app.config['MAX_MESSAGES'] + 5):
#         client.post('/chat/message',
#                    json={'message': f'Test message {i}'},
#                    content_type='application/json')
#
#     response = client.get('/chat/history')
#     data = json.loads(response.data)
#     assert len(data) <= app.config['MAX_MESSAGES']
