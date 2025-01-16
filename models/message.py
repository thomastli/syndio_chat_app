from datetime import datetime

from pydantic import BaseModel


class Message(BaseModel):
    """Defines a message data model"""
    user: str
    message: str
    timestamp: datetime
