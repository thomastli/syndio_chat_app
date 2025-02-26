import logging
import random

from ai.base_ai import AIModel

logger = logging.getLogger(__name__)

DUMMY_RESPONSES = [
    "Hi there! I'm a simulated AI assistant.",
    "Hello! This is a placeholder AI response.",
    "I'm just a dummy function pretending to be AI.",
    "That's an interesting point! Let me think about it...",
    "I understand what you're saying. Please tell me more!"
]


class DummyAI(AIModel):
    """Wrapper class that implements a dummy AI model"""

    def get_ai_response(self, user_message: str) -> str:
        """
        Get AI response for user message.

        Uses randomized dummy responses.

        Args:
            user_message: The message from the user

        Returns:
            The AI response message
        """
        # See ai/gpt_40_mini.py for an example of how to implement an AI response with a real LLM

        # Splunk logging:
        # logger.info('AI request', extra={
        #     'event_type': 'ai_call',
        #     'component': 'ai',
        #     'ai_model': 'dummy',
        #     'user_message': user_message
        # })
        logger.info(f"Generating AI response for message: {user_message}")
        return random.choice(DUMMY_RESPONSES)
