import logging
import sys
# from logtail import LogtailHandler

logger = logging.getLogger()

formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(message)s"
)

stream_handler = logging.StreamHandler(sys.stdout)
# file_handler = logging.FileHandler('app.log')
# better_stack_handler = LogtailHandler(source_token=token)

stream_handler.setFormatter(formatter)
# file_handler.setFormatter(formatter)

# logger.handlers = [stream_handler, file_handler, better_stack_handler]
logger.handlers = [stream_handler]

logger.setLevel(logging.WARNING)

# https://telemetry.betterstack.com/team/318148/tail
# https://www.youtube.com/watch?v=1RLFSOwpf88&t=646s
