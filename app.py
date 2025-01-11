from flask import Flask, request, jsonify, render_template, Response
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import List

import logging
import os

from ai.dummy_ai import DummyAI
from ai.gpt_4o_mini import GPT4oMini
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
app.config['MAX_MESSAGES'] = int(os.getenv('MAX_MESSAGES', '100'))
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
        return jsonify({'error': 'Internal server error'}), 500


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

        if not data or 'message' not in data:
            logger.warning("Invalid message format received")
            return jsonify({'error': 'Invalid request format'}), 400

        user_message = data['message'].strip()
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400

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

        return jsonify({'status': 'success'}), 200

    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/chat/history', methods=['GET'])
def get_history() -> (Response, int):
    """ Retrieve chat history

    :return:
        The response containing the chat history
    """
    try:
        return jsonify([dict(msg) for msg in messages]), 200
    except Exception as e:
        logger.error(f"Error retrieving chat history: {str(e)}")
        return jsonify({'error': 'Error retrieving chat history'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', '5000')))