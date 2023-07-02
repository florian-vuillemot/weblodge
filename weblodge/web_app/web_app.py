from typing import List, Dict

from weblodge.config import Item as ConfigItem

from .build import Build
from .deploy import Deploy


def build_config() -> List[ConfigItem]:
    """
    Return the build configuration.
    """
    return Build.config


def build(config: Dict[str, str]) -> None:
    """
    Build the application from the config.
    """
    _config = {
        k: v for k, v in config.items() if k in Build.config
    }
    Build(**_config).build()


def deploy_config() -> List[ConfigItem]:
    """
    Return the deployment configuration.
    """
    return Deploy.config


def deploy(config: Dict[str, str]) -> None:
    """
    Deploy the application from the config.
    """
    _config = {
        k: v for k, v in config.items() if k in Deploy.config
    }
    return Deploy(**_config).deploy()
