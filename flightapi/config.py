from os import environ
from typing import Optional

from pyaml import yaml

from .log_config import get_logger
from .schemas.config import Config

LOGGER = get_logger(__name__)

SERVICE_CONFIG: Optional[Config] = None


def init_from_yaml(yaml_config_dict: dict):
    global SERVICE_CONFIG
    """Initialize the global configuration variables by parsing the provided YAML."""
    SERVICE_CONFIG = Config(**yaml_config_dict)


class MissingConfigException(Exception):
    """Raised when the configuration is missing"""

    pass


def init_from_file():
    """Initialize the global configuration variables by parsing the CONFIG YAML."""
    config_path = environ.get("FLIGHTAPI_CONFIG", "globalfootprint/etc/config.yml")
    if config_path is None:
        raise MissingConfigException(
            "Missing configuration, please set the "
            "'GLOBALFOOTPRINT_CONFIG' environmental variable "
            "to point to the config file location."
        )

    with open(config_path, "rb") as config:
        loaded_config = yaml.load(config, Loader=yaml.FullLoader)
        init_from_yaml(loaded_config)

    LOGGER.info(
        f"Configurations were properly loaded: \nCONFIG: {SERVICE_CONFIG.dict()}"
    )
