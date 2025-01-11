from abc import ABC, abstractmethod

class AIModel(ABC):
    """Classes that defines an interface for communicating with AI models"""

    @abstractmethod
    def get_ai_response(self, user_message: str) -> str:
        """
        Get response from AI for a user message.

        Args:
            user_message: The message from the user

        Returns:
            str: The response from the AI
        """
        pass
