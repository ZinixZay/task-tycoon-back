from enum import Enum
from src.jwt_strategy.dto import REFRESH_TOKEN_LABEL, ACCESS_TOKEN_LABEL


class TokenTypeEnum(Enum):
    ACCESS_TOKEN = ACCESS_TOKEN_LABEL
    REFRESH_TOKEN = REFRESH_TOKEN_LABEL
