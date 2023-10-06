"""
Web App facade.

Wrapp all actions related to the Azure Web App.
"""
import logging

from typing import Callable, Iterable, List, Dict, Optional, Tuple

from weblodge._azure import AzureService, AzureWebApp, AzureAppServiceSku
from weblodge.config import Item as ConfigItem

from ._all import _all as _all_az_web_app
from .build import BuildConfig, build as _build
from .delete import DeleteConfig, delete as _delete
from .deploy import DeploymentConfig, deploy as _deploy
from .exceptions import RequirementsFileNotFound, EntryPointFileNotFound, FlaskAppNotFound
from .logs import LogsConfig, logs as _logs
from .github import GitHubConfig, github, GitHubWorkflow
from .tiers import TiersConfig, tiers as _tiers


logger = logging.getLogger('weblodge')


class WebApp:
    """
    Represent a Flask Web Application deploy on Azure.
    """
    def __init__(
        self,
        config_loader: Callable[[List[ConfigItem]], Dict[str, str]],
        azure_service: AzureService,
        web_app: AzureWebApp = None
    ):
        self.config_loader = config_loader
        self._web_app = web_app
        self.azure_service = azure_service

    @property
    def name(self) -> Optional[str]:
        """
        Return the name of the WebApp if exists, None otherwise.
        """
        return self._web_app.name if self._web_app else None

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
        self._web_app = _deploy(self.azure_service, deployment_config)
        logger.info('Successfully deployed.')

        return True, config

    def url(self) -> str:
        """
        Get the URL of the deployed application.
        """
        return f'https://{self._web_app.domain}'

    def delete(self, config: Dict[str, str] = None) -> Tuple[bool, Dict[str, str]]:
        """
        Delete the application.
        """
        if config is None:
            config = {'subdomain': self._web_app.name}

        config = self.config_loader(DeleteConfig.items, config)
        delete_config = DeleteConfig(**config)

        logger.info('Deleting...')
        _delete(self.azure_service, delete_config)
        self._web_app = None
        logger.info('Successfully deleted.')

        return True, config

    def github(self, config: Dict[str, str]) -> Tuple[Dict[str, str], Optional[GitHubWorkflow]]:
        """
        Create a GitHub Workflow for the application.
        Workflow is None if the application has been deleted.
        """
        config = self.config_loader(GitHubConfig.items, config)
        github_config = GitHubConfig(**config)
        workflow = github(self.azure_service, github_config)
        # The deleted configuration is not one we want to propagate.
        config.pop('delete', None)
        return config, workflow

    def print_logs(self, config: Dict[str, str]):
        """
        Print the application logs.
        This method is blocking and never returns.
        """
        logs_config = LogsConfig(
            **self.config_loader(LogsConfig.items, config)
        )
        _logs(self.azure_service, logs_config)

    def exists(self) -> bool:
        """
        Return True if the application exists, False otherwise.
        """
        return self._web_app.exists()

    def infrastruture_exists(self) -> bool:
        """
        Return True if the application infrastructure exists, False otherwise.
        """
        return self._web_app.resource_group.exists()

    def all(self, config_loader: Callable[[List[ConfigItem]], Dict[str, str]] = None) -> Iterable['WebApp']:
        """
        Return all WebApp created by WebLodge.
        """
        yield from (
            WebApp(config_loader, self.azure_service, web_app)
            for web_app in _all_az_web_app(self.azure_service)
        )

    def tiers(self, config: Dict[str, str]) -> List[AzureAppServiceSku]:
        """
        Return all tiers of the application.
        """
        config = self.config_loader(TiersConfig.items, config)
        tier_config = TiersConfig(**config)
        return _tiers(self.azure_service, tier_config)
