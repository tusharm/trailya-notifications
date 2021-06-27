from config.config import Config
from datasets.nsw_dataset import NSWDataset


class NSWConfig(Config):
    def __init__(self):
        super().__init__()

    def dataset_service(self):
        return NSWDataset()
