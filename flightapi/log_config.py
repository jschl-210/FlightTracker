import logging
import os
import sys
from logging.handlers import RotatingFileHandler

LOGGER_FORMAT = (
    "%(levelname)s: %(asctime)s - %(filename)s:%(funcName)s:%(lineno)d\t - %(message)s"
)

log_filename = "logs/flighttracker_log.log"
os.makedirs(os.path.dirname(log_filename), exist_ok=True)

handlers: list[logging.Handler] = [
    RotatingFileHandler(filename=log_filename),
    logging.StreamHandler(sys.stdout),
]


logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    handlers=handlers,
    format=LOGGER_FORMAT,
)


def get_logger(name) -> logging.Logger:
    logger = logging.getLogger(name)
    return logger
