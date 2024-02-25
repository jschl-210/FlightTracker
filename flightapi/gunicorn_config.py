"""Gunicorn configuration.

Environment variables:
    - FLIGHTAPI_BIND: Default 0.0.0.0:8000, The host and IP to set the bind argument
    - FLIGHTAPI_WORKERS: Default CPU count, The number of gunicorn workers
    - FLIGHTAPI_LOG_LEVEL: Default info, the log level for the application
"""

import multiprocessing
from os import environ

from flightapi.log_config import get_logger

LOGGER = get_logger(__name__)

bind = environ.get("FLIGHTAPI_BIND", "0.0.0.0:8000")
workers = int(environ.get("FLIGHTAPI_WORKERS", multiprocessing.cpu_count()))
log_level = environ.get("FLIGHTAPI_LOG_LEVEL", "info")
environment_domain = environ.get("ENVIRONMENT_DOMAIN")
worker_class = "uvicorn.workers.UvicornWorker"
threads = 4
