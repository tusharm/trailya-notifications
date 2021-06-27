import os

from utils.secrets import get_secret


class ConfigError(Exception):
    def __init__(self, config: str):
        super().__init__(f'Missing config \"{config}\"')


class Config:
    def __init__(self):
        maps_api_key_id = self._getenv_or_raise('MAPS_API_KEY_ID')
        self._maps_api_key = get_secret(maps_api_key_id)

    def maps_api_key(self):
        return self._maps_api_key

    def dataset_service(self):
        raise NotImplementedError

    def _getenv_or_raise(self, config_name: str):
        api_key_id = os.getenv(config_name)
        if api_key_id:
            return api_key_id

        raise ConfigError(config_name)

