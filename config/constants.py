from enum import Enum, IntEnum, StrEnum


class AppConfig(Enum):
    APP_HOST = "0.0.0.0"
    APP_PORT = 5000
    MAX_MESSAGE_LIMIT = "100"

class Constants(StrEnum):
    ERROR_FIELD = "error"
    MESSAGE_FIELD = "message"
    STATUS_FIELD = "status"
    SUCCESS_FIELD = "success"

class Environment(StrEnum):
    PORT_VARIABLE = "PORT"

class StatusCodes(IntEnum):
    SUCCESS_CODE = 200
    BAD_REQUEST_ERROR_CODE = 400
    INTERNAL_SERVER_ERROR_CODE = 500