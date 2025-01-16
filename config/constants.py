from enum import Enum, IntEnum, StrEnum


class AppConfig(Enum):
    """Defines Flask application related configuration constants"""
    APP_HOST = "127.0.0.1"
    APP_PORT = 5000
    MAX_MESSAGES = "100"


class Constants(StrEnum):
    """Defines field constants"""
    CONTENT_FIELD = "content"
    DEBUG_FIELD = "DEBUG"
    ERROR_FIELD = "error"
    ID_FIELD = "_id"
    MAX_MESSAGES_FIELD = "MAX_MESSAGES"
    MESSAGE_FIELD = "message"
    MONGO_URI_FIELD = "MONGO_URI"
    PORT_FIELD = "PORT"
    ROLE_FIELD = "role"
    STATUS_FIELD = "status"
    SUCCESS_FIELD = "success"
    TESTING_FIELD = "TESTING"
    TIMESTAMP_FIELD = "timestamp"
    USER_FIELD = "user"


class EnvironmentVariables(StrEnum):
    """Defines environment variable name constants"""
    APP_HOST_VARIABLE = "APP_HOST"
    DEBUG_VARIABLE = "DEBUG"
    MAX_MESSAGES_VARIABLE = "MAX_MESSAGES"
    MONGO_URI_VARIABLE = "MONGO_URI"
    OPENAI_API_KEY_VARIABLE = "OPEN_AI_API_KEY"
    PORT_VARIABLE = "PORT"


class StatusCodes(IntEnum):
    """Defines request status codes as constants"""
    SUCCESS_CODE = 200
    BAD_REQUEST_ERROR_CODE = 400
    INTERNAL_SERVER_ERROR_CODE = 500
