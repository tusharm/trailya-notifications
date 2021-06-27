from .nsw_config import NSWConfig
from .vic_config import VictoriaConfig


def config_factory(location: str):
    if location == 'VIC':
        return VictoriaConfig()

    if location == 'NSW':
        return NSWConfig()

    return None
