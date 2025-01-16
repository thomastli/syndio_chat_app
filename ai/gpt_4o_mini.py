import logging
import os

from openai import OpenAI

from ai.base_ai import AIModel
from config.constants import EnvironmentVariables, Constants

# For splunk logging:
# import traceback

OPENAI_API_KEY = os.environ.get(EnvironmentVariables.OPENAI_API_KEY_VARIABLE)

logger = logging.getLogger(__name__)


class GPT4oMini(AIModel):
    """Wrapper class that implements support for the GPT-4o Mini model"""

    def get_ai_response(self, user_message: str) -> str:
        """
        Get AI response for user message.

        Args:
            user_message: The message from the user

        Returns:
            The AI response message
        """
        try:

            client = OpenAI(api_key=OPENAI_API_KEY)

            # Splunk logging:
            # logger.info('AI call', extra={
            #     'event_type': 'ai_call',
            #     'component': 'ai',
            #     'error_message': str(e),
            #     'user_message': user_message
            # })
            logger.info(f"Generating AI response for message: {user_message}")
            response = client.chat.completions.create(
                messages=[
                    {
                        Constants.ROLE_FIELD: "user",
                        Constants.CONTENT_FIELD: user_message
                    }
                ],
                model="gpt-4o-mini",
            )

            return response.choices[0].message.content

        except Exception as e:
            # Splunk logging:
            # logger.error('AI response error', extra={
            #     'event_type': 'error',
            #     'component': 'ai',
            #     'error_message': str(e),
            #     'user_message': user_message,
            #     'stack_trace': traceback.format_exc()
            # })
            logger.error(f"Error calling LLM API: {str(e)}")
            return "I apologize, but I'm having trouble processing your request."
