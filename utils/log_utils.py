from logging.handlers import RotatingFileHandler
# from splunk_handler import SplunkHandler

import logging
# import os


def configure_logger() -> logging.Logger:
    # Splunk logging implementation
    #
    # SPLUNK_HOST = os.environ.get('SPLUNK_HOST', 'splunk.example.com')
    # SPLUNK_PORT = int(os.environ.get('SPLUNK_PORT', 8089))
    # SPLUNK_TOKEN = os.environ.get('SPLUNK_TOKEN', 'your-splunk-token')
    # SPLUNK_INDEX = os.environ.get('SPLUNK_INDEX', 'chat_app_logs')
    # SPLUNK_SOURCE = os.environ.get('SPLUNK_SOURCE', 'chat_application')
    #
    # splunk_handler = SplunkHandler(
    #     host=SPLUNK_HOST,
    #     port=SPLUNK_PORT,
    #     token=SPLUNK_TOKEN,
    #     index=SPLUNK_INDEX,
    #     source=SPLUNK_SOURCE,
    #     sourcetype='chat_app',
    #     verify=True
    # )
    #
    # # Configure Splunk handler
    # splunk_handler.setLevel(logging.INFO)
    # logger.addHandler(splunk_handler)
    # return logger


    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    handler = RotatingFileHandler('chat_app.log', maxBytes=10000, backupCount=3)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
