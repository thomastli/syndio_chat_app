import random

from ai.base_ai import AIModel

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
        Get AI response for user message. Currently uses dummy responses,
        but could be replaced with real LLM API call in production.

        Args:
            user_message: The message from the user

        Returns:
            str: AI response message
        """
        # Example of how we'd integrate with a real LLM in production:
        # try:
        #     client = OpenAI(
        #         api_key=os.environ.get("OPENAI_API_KEY"),
        #     )
        #
        #     response = client.chat.completions.create(
        #         messages=[
        #             {
        #                 "role": "user",
        #                 "content": user_message
        #             }
        #         ],
        #         model="gpt-4o-mini",
        #     )
        #
        #     return response.choices[0].message.content
        #
        # except Exception as e:
        #     logger.error(f"Error calling LLM API: {str(e)}")
        #     return "I apologize, but I'm having trouble processing your request."

        return random.choice(DUMMY_RESPONSES)