from enum import Enum, IntEnum, StrEnum


class AppConfig(Enum):
    APP_HOST = "0.0.0.0"
    APP_PORT = 5000
    MAX_MESSAGE_LIMIT = "100"

class Constants(StrEnum):
    CONTENT_FIELD = "content"
    ERROR_FIELD = "error"
    ID_FIELD = "_id"
    MESSAGE_FIELD = "message"
    ROLE_FIELD = "role"
    STATUS_FIELD = "status"
    SUCCESS_FIELD = "success"
    TIMESTAMP_FIELD = "timestamp"
    USER_FIELD = "user"

class Environment(StrEnum):
    MONGO_URI_VARIABLE = "MONGO_URI"
    OPENAI_API_KEY_VARIABLE = "OPEN_AI_API_KEY"
    PORT_VARIABLE = "PORT"

class StatusCodes(IntEnum):
    SUCCESS_CODE = 200
    BAD_REQUEST_ERROR_CODE = 400
    INTERNAL_SERVER_ERROR_CODE = 500