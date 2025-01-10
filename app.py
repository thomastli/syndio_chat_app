from flask import Flask, request, jsonify, render_template, Response
from datetime import datetime
import logging
import random
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import os
from logging.handlers import RotatingFileHandler
import json

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
handler = RotatingFileHandler('chat_app.log', maxBytes=10000, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# In production, these would be environment variables
app.config['MAX_MESSAGES'] = int(os.getenv('MAX_MESSAGES', '100'))
app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() == 'true'


@dataclass
class Message:
    """Data class for chat messages"""
    user: str
    message: str
    timestamp: datetime

    def to_dict(self) -> Dict:
        """Convert message to dictionary format"""
        return {
            'user': self.user,
            'message': self.message,
            'timestamp': self.timestamp.isoformat()
        }


# In-memory storage for messages
messages: List[Message] = []

# AI response configurations
DUMMY_RESPONSES = [
    "Hi there! I'm a simulated AI assistant.",
    "Hello! This is a placeholder AI response.",
    "I'm just a dummy function pretending to be AI.",
    "That's an interesting point! Let me think about it...",
    "I understand what you're saying. Please tell me more!"
]


def get_ai_response(user_message: str) -> str:
    """
    Get AI response for user message. Currently uses dummy responses,
    but could be replaced with real LLM API call in production.

    Args:
        user_message: The message from the user

    Returns:
        str: AI response message
    """
    # Example of how we'd integrate with a real LLM in production:
    # try:
    #     response = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=[{"role": "user", "content": user_message}]
    #     )
    #     return response.choices[0].message.content
    # except Exception as e:
    #     logger.error(f"Error calling LLM API: {str(e)}")
    #     return "I apologize, but I'm having trouble processing your request."

    logger.info(f"Generating AI response for: {user_message}")
    return random.choice(DUMMY_RESPONSES)


@app.route('/')
def home() -> Response:
    """Serve the chat interface"""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error serving home page: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/chat/message', methods=['POST'])
def send_message() -> Response:
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
        ai_response = get_ai_response(user_message)
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
def get_history() -> Response:
    """Retrieve chat history"""
    try:
        return jsonify([msg.to_dict() for msg in messages]), 200
    except Exception as e:
        logger.error(f"Error retrieving chat history: {str(e)}")
        return jsonify({'error': 'Error retrieving chat history'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', '5000')))