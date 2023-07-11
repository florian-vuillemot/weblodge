"""
Web App function to simplify the build, deploy and delete process.
"""
import functools
from typing import List, Dict

from weblodge.config import Item as ConfigItem

from .deploy import Deploy
from .delete import Delete


# pylint: disable=missing-function-docstring
def filter_config(retrieve_config):
    def _filter_config(func) -> Dict[str, str]:
        @functools.wraps(func)
        def __filter_config(config: Dict[str, str]):
            _config = {
                k: v for k, v in config.items() if k in retrieve_config()
            }
            return func(_config)
        return __filter_config
    return _filter_config


def deploy_config() -> List[ConfigItem]:
    """
    Return the deployment configuration.
    """
    return Deploy.config


@filter_config(deploy_config)
def deploy(config: Dict[str, str]) -> None:
    """
    Deploy the application from the config.
    """
    config = {
        **config,
        'tags': {
            'environment': config['environment'],
            'managed-by': 'weblodge'
        }
    }
    return Deploy(**config).deploy()


def delete_config() -> List[ConfigItem]:
    """
    Return the delete configuration.
    """
    return Delete.config


@filter_config(delete_config)
def delete(config: Dict[str, str]) -> None:
    """
    Delete the application from the config.
    """
    return Delete(**config).delete()
