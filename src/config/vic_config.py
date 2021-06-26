from config.config import Config
from datasets.victoria_dataset import VictoriaDataset
from utils.secrets import get_secret


class VictoriaConfig(Config):
    def __init__(self):
        super().__init__()

        api_key_id = self._getenv_or_raise('VIC_API_KEY_ID')
        self._dataset_api_key = get_secret(api_key_id)

    def dataset_api_key(self):
        return self._dataset_api_key

    def dataset_creator(self):
        return VictoriaDataset.create
