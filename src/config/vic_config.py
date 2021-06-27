from config.config import Config
from datasets.victoria_dataset import VictoriaDataset
from utils.secrets import get_secret


class VictoriaConfig(Config):
    def __init__(self):
        super().__init__()

        api_key_id = self._getenv_or_raise('VIC_API_KEY_ID')
        self._dataset_api_key = get_secret(api_key_id)

    def dataset_service(self):
        return VictoriaDataset(self._dataset_api_key)
