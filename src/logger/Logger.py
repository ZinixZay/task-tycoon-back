from loguru import logger


class Log:
    @classmethod
    def debug(cls, msg: str) -> None:
        logger.debug(msg)

    @classmethod
    def info(cls, msg: str) -> None:
        logger.info(msg)

    @classmethod
    def warning(cls, msg: str) -> None:
        logger.warning(msg)

    @classmethod
    def error(cls, msg: str) -> None:
        logger.error(msg)
