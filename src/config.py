import json


class Config:
    __config_path = "../data/config.json"
    __config = None

    @staticmethod
    def config() -> dict:
        if Config.__config is None:
            with open(Config.__config_path) as f:
                Config.__config = json.load(f)

        return Config.__config
