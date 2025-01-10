from dataclasses import dataclass
from datetime import datetime
from typing import Dict


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
