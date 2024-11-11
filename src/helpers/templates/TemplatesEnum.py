from enum import Enum


class CacheTemplatesEnum(Enum):
    CONFIRMATION_RECORD = 'confirmation_$1'


class TemplatesEnum(Enum):
    CACHE = CacheTemplatesEnum
