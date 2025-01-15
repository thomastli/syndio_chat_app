from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template, Response
from datetime import datetime

import os

from ai.dummy_ai import DummyAI
# from ai.gpt_4o_mini import GPT4oMini
from config.constants import AppConfig, Constants, EnvironmentVariables, StatusCodes
from db.mongo_db import MongoDb
from models.message import Message
from utils.log_utils import configure_logger
from utils.message_utils import clean_mongo_id

load_dotenv()
MONGO_URI = os.environ.get(EnvironmentVariables.MONGO_URI_VARIABLE, "mongodb://mongodb:27017/chat_app")
OPENAI_API_KEY = os.environ.get(EnvironmentVariables.OPENAI_API_KEY_VARIABLE)

# Initialize Flask app
app = Flask(__name__)
app.config[EnvironmentVariables.MONGO_URI_VARIABLE] = MONGO_URI

logger = configure_logger()

# In production, these would be environment variables
app.config['MAX_MESSAGES'] = int(os.getenv(EnvironmentVariables.MAX_MESSAGES_VARIABLE, AppConfig.MAX_MESSAGES.value))
app.config['DEBUG'] = os.getenv(EnvironmentVariables.DEBUG_VARIABLE, 'False').lower() == 'true'

# AI response using dummy AI model
ai = DummyAI()
# AI responses using GPT 4o-mini model
# ai = GPT4oMini()

# Database configuration
db = MongoDb(app)


@app.route('/')
def home() -> (Response, int):
    """Serve the chat interface"""
    try:
        # Splunk logging:
        # logger.info('Home page accessed', extra={
        #     'event_type': 'page_access',
        #     'endpoint': '/',
        #     'client_ip': request.remote_addr,
        #     'user_agent': request.user_agent.string
        # })
        logger.info('Retrieved home page')
        return render_template('index.html')
    except Exception as e:
        # Splunk logging:
        # logger.error('Home page error', extra={
        #     'event_type': 'error',
        #     'endpoint': '/',
        #     'error_message': str(e),
        #     'client_ip': request.remote_addr,
        #     'stack_trace': traceback.format_exc()
        # })
        logger.error(f"Error serving home page: {str(e)}")
        return jsonify({Constants.ERROR_FIELD: 'Internal server error'}), StatusCodes.INTERNAL_SERVER_ERROR_CODE


@app.route('/chat/message', methods=['POST'])
def send_message() -> (Response, int):
    """
    Handle incoming chat messages

    Expected request body:
    {
        "user": "User",
        "message": "User's message here",
        "timestamp":
    }
    """
    try:
        data = request.get_json()

        if not data or Constants.MESSAGE_FIELD not in data:
            # Splunk logging:
            # logger.warning('Invalid message format', extra={
            #     'event_type': 'validation_error',
            #     'endpoint': '/chat/message',
            #     'client_ip': request.remote_addr,
            #     'request_data': data
            # })
            logger.warning("Invalid message format received")
            return jsonify({Constants.ERROR_FIELD: 'Invalid request format'}), StatusCodes.BAD_REQUEST_ERROR_CODE

        user_message = data[Constants.MESSAGE_FIELD].strip()
        if not user_message:
            # Splunk logging:
            # logger.warning('Message cannot be empty', extra={
            #     'event_type': 'validation_error',
            #     'endpoint': '/chat/message',
            #     'client_ip': request.remote_addr,
            #     'request_data': data
            # })
            logger.warning("Message cannot be empty")
            return jsonify({Constants.ERROR_FIELD: 'Message cannot be empty'}), StatusCodes.BAD_REQUEST_ERROR_CODE

        # Store user message
        user_msg = Message(
            user="User",
            message=user_message,
            timestamp=datetime.now()
        )
        db.insert_message(user_msg)
        # Splunk logging:
        # logger.info('User message received', extra={
        #     'event_type': 'user_message',
        #     'endpoint': '/chat/message',
        #     'user': user_msg.user,
        #     'message_length': len(user_msg.message),
        #     'timestamp': user_msg.timestamp.isoformat(),
        #     'client_ip': request.remote_addr
        # })
        logger.info(
            f"Message from user: {user_msg.user}, message = {user_msg.message}, timestamp = {user_msg.timestamp}")

        # Get and store AI response
        ai_response = ai.get_ai_response(user_message)
        ai_msg = Message(
            user="AI",
            message=ai_response,
            timestamp=datetime.now()
        )
        db.insert_message(ai_msg)
        # Splunk logging:
        # logger.info('AI response generated', extra={
        #     'event_type': 'ai_response',
        #     'endpoint': '/chat/message',
        #     'response_length': len(ai_response),
        #     'processing_time': (datetime.now() - user_msg.timestamp).total_seconds(),
        #     'timestamp': ai_msg.timestamp.isoformat()
        # })
        logger.info(
            f"Message from user: {ai_msg.user}, message = {ai_msg.message}, timestamp = {ai_msg.timestamp}")

        # Maintain message limit
        # while len(messages) > app.config['MAX_MESSAGES']:
        #     messages.pop(0)

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
        messages = db.retrieve_messages()
        cleaned_messages = clean_mongo_id(messages)
        # Splunk logging:
        # logger.info('Chat history retrieved', extra={
        #     'event_type': 'history_retrieval',
        #     'endpoint': '/chat/history',
        #     'message_count': len(cleaned_messages),
        #     'client_ip': request.remote_addr
        # })
        logger.info(f"Retrieved {len(cleaned_messages)} chat messages from history")
        return jsonify(cleaned_messages), StatusCodes.SUCCESS_CODE
    except Exception as e:
        # Splunk logging:
        # logger.error('Chat history retrieval error', extra={
        #     'event_type': 'error',
        #     'endpoint': '/chat/history',
        #     'error_message': str(e),
        #     'client_ip': request.remote_addr,
        #     'stack_trace': traceback.format_exc()
        # })
        logger.error(f"Error retrieving chat history: {str(e)}")
        return jsonify({Constants.ERROR_FIELD: 'Error retrieving chat history'}), StatusCodes.INTERNAL_SERVER_ERROR_CODE


if __name__ == '__main__':
    port = int(os.getenv(EnvironmentVariables.PORT_VARIABLE, AppConfig.APP_PORT.value))
    app.run(host=AppConfig.APP_HOST.value, port=port)
