from flask import Flask, request, jsonify, render_template, Response
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import List

import logging
import os

from ai.dummy_ai import DummyAI
from ai.gpt_4o_mini import GPT4oMini
from config.constants import AppConfig, Constants, Environment, StatusCodes
from models.message import Message


# Initialize Flask app
app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
handler = RotatingFileHandler('chat_app.log', maxBytes=10000, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


# In production, these would be environment variables
app.config['MAX_MESSAGES'] = int(os.getenv('MAX_MESSAGES', AppConfig.MAX_MESSAGE_LIMIT.value))
app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() == 'true'


# In-memory storage for messages
messages: List[Message] = []

# AI response configurations
ai = DummyAI()

@app.route('/')
def home() -> (Response, int):
    """Serve the chat interface"""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error serving home page: {str(e)}")
        return jsonify({'error': 'Internal server error'}), StatusCodes.INTERNAL_SERVER_ERROR_CODE


@app.route('/chat/message', methods=['POST'])
def send_message() -> (Response, int):

    """
    Handle incoming chat messages

    Expected request body:
    {
        "message": "User's message here"
    }
    """
    try:
        data = request.get_json()

        if not data or Constants.MESSAGE_FIELD not in data:
            logger.warning("Invalid message format received")
            return jsonify({'error': 'Invalid request format'}), StatusCodes.BAD_REQUEST_ERROR_CODE

        user_message = data[Constants.MESSAGE_FIELD].strip()
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), StatusCodes.BAD_REQUEST_ERROR_CODE

        # Store user message
        messages.append(Message(
            user="User",
            message=user_message,
            timestamp=datetime.now()
        ))

        # Get and store AI response
        ai_response = ai.get_ai_response(user_message)
        messages.append(Message(
            user="AI",
            message=ai_response,
            timestamp=datetime.now()
        ))

        # Maintain message limit
        while len(messages) > app.config['MAX_MESSAGES']:
            messages.pop(0)

        return jsonify({Constants.STATUS_FIELD: 'success'}), StatusCodes.SUCCESS_CODE

    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        return jsonify({Constants.ERROR_FIELD: 'Internal server error'}), StatusCodes.INTERNAL_SERVER_ERROR_CODE


@app.route('/chat/history', methods=['GET'])
def get_history() -> (Response, int):
    """ Retrieve chat history

    :return:
        The response containing the chat history
    """
    try:
        return jsonify([dict(msg) for msg in messages]), StatusCodes.SUCCESS_CODE
    except Exception as e:
        logger.error(f"Error retrieving chat history: {str(e)}")
        return jsonify({'error': 'Error retrieving chat history'}), StatusCodes.INTERNAL_SERVER_ERROR_CODE


if __name__ == '__main__':
    app.run(host=AppConfig.APP_HOST.value, port=int(os.getenv(Environment.PORT_VARIABLE, AppConfig.APP_PORT.value)))