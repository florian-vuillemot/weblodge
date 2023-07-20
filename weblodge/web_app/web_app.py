"""
Web App facade.

Wrapp all actions related to the Azure Web App.
"""
import logging

from typing import Callable, List, Dict, Tuple

from weblodge.config import Item as ConfigItem

from .logs import LogsConfig, logs as _logs
from .delete import DeleteConfig, delete as _delete
from .deploy import DeploymentConfig, deploy as _deploy
from .build import BuildConfig, build as _build
from .exceptions import RequirementsFileNotFound, EntryPointFileNotFound, FlaskAppNotFound


logger = logging.getLogger('weblodge')


class WebApp:
    """
    Represent a Flask Web Application deploy on Azure.
    """
    def __init__(self, config_loader: Callable[[List[ConfigItem]], Dict[str, str]]):
        self.config_loader = config_loader
        self._web_app = None

    def build(self, config: Dict[str, str]) -> Tuple[bool, Dict[str, str]]:
        """
        Build the application.
        """
        config = self.config_loader(BuildConfig.items, config)
        build_config = BuildConfig(**config)

        logger.info('Building...')
        try:
            _build(build_config)
        except RequirementsFileNotFound:
            logger.critical(f"Requirements file '{build_config.requirements}' not found.")
            logger.critical('Build failed.')
            return False, build_config
        except EntryPointFileNotFound:
            logger.critical(f"Entry point file '{build_config.entry_point}' not found.")
            logger.critical('Build failed.')
            return False, build_config
        except FlaskAppNotFound:
            logger.critical(f"Can not find the Flask application '{build_config.flask_app}' in the file '{build_config.entry_point}'.") # pylint: disable=line-too-long
            logger.critical('Build failed.')
            return False, build_config

        logger.info('Successfully built.')
        return True, config

    def deploy(self, config: Dict[str, str]) -> Tuple[bool, Dict[str, str]]:
        """
        Deploy an application.
        """
        config = self.config_loader(DeploymentConfig.items, config)
        deployment_config = DeploymentConfig(**config)

        logger.info('Deploying...')
        self._web_app = _deploy(deployment_config)
        logger.info('Successfully deployed.')

        return True, config

    def url(self):
        """
        Get the URL of the deployed application.
        """
        return f'https://{self._web_app.domain}'

    def delete(self, config: Dict[str, str]) -> Tuple[bool, Dict[str, str]]:
        """
        Delete the application.
        """
        config = self.config_loader(DeleteConfig.items, config)
        delete_config = DeleteConfig(**config)

        logger.info('Deleting...')
        _delete(delete_config)
        self._web_app = None
        logger.info('Successfully deleted.')

        return True, config

    def print_logs(self, config: Dict[str, str]):
        """
        Print the application logs.
        This method is blocking and never returns.
        """
        logs_config = LogsConfig(
            **self.config_loader(LogsConfig.items, config)
        )
        _logs(logs_config)
