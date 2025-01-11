from openai import OpenAI

import logging
import os

from ai.base_ai import AIModel

logger = logging.getLogger(__name__)

class GPT4oMini(AIModel):
    """Wrapper class that implements support for the GPT-4o Mini model"""

    def get_ai_response(self, user_message: str) -> str:
        """
        Get AI response for user message. Currently uses dummy responses,
        but could be replaced with real LLM API call in production.

        Args:
            user_message: The message from the user

        Returns:
            str: AI response message
        """
        try:
            client = OpenAI(
                api_key=os.environ.get("OPENAI_API_KEY"),
            )

            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                model="gpt-4o-mini",
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error calling LLM API: {str(e)}")
            return "I apologize, but I'm having trouble processing your request."
