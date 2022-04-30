import configparser
from typing import Dict


def read_config(config_file: str) -> Dict:
    config = configparser.ConfigParser()
    config.read(config_file)

    default = config["DEFAULT"]
    return {
        k: default[k] for k in default
    }
