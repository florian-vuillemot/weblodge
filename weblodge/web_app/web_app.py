"""
Web App facade.

Wrapp all actions related to the Azure Web App.
"""
import logging

from typing import Callable, Iterable, List, Dict, Optional, Tuple

from weblodge._azure import AzureService, AzureWebApp
from weblodge.config import Item as ConfigItem

from .build import BuildConfig, build as _build
from .delete import DeleteConfig, delete as _delete
from .deploy import DeploymentConfig, deploy as _deploy
from .exceptions import RequirementsFileNotFound, EntryPointFileNotFound, FlaskAppNotFound, \
    InvalidTier, WebAppNotSetException
from .logs import LogsConfig, logs as _logs
from .github import GitHubConfig, github, GitHubWorkflow
from .tiers import TiersConfig, tiers as _tiers, WebAppTier


logger = logging.getLogger('weblodge')


class WebApp:
    """
    Represent a Flask Web Application deploy on Azure.
    """
    def __init__(
        self,
        config_loader: Callable[[List[ConfigItem], Optional[Dict[str, str]]], Dict],
        azure_service: AzureService,
        web_app: Optional[AzureWebApp] = None
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
            return False, {}
        except EntryPointFileNotFound:
            logger.critical(f"Entry point file '{build_config.entry_point}' not found.")
            logger.critical('Build failed.')
            return False, {}
        except FlaskAppNotFound:
            logger.critical(f"Can not find the Flask application '{build_config.flask_app}' in the file '{build_config.entry_point}'.") # pylint: disable=line-too-long
            logger.critical('Build failed.')
            return False, {}

        logger.info('Successfully built.')
        return True, config

    def deploy(self, config: Dict[str, str]) -> Tuple[bool, Dict[str, str], WebAppTier]:
        """
        Deploy an application.
        """
        config = self.config_loader(DeploymentConfig.items, config)
        deployment_config = DeploymentConfig(**config)

        tier = self._get_tier(config, deployment_config.tier)

        logger.info('Deploying...')
        self._web_app = _deploy(self.azure_service, deployment_config)
        logger.info('Successfully deployed.')

        return True, config, tier

    def url(self) -> Optional[str]:
        """
        Get the URL of the deployed application.
        """
        if not self._web_app:
            raise WebAppNotSetException('The web app must be set.')
        return f'https://{self._web_app.domain}'

    def delete(self, config: Optional[Dict[str, str]] = None) -> Tuple[bool, Dict[str, str]]:
        """
        Delete the application.
        """
        if config is None:
            if not self._web_app:
                raise WebAppNotSetException('The web app must be set.')
            config = {'subdomain': self._web_app.name}

        new_config = config = self.config_loader(DeleteConfig.items, config)
        delete_config = DeleteConfig(**new_config)

        logger.info('Deleting...')
        _delete(self.azure_service, delete_config)
        self._web_app = None
        logger.info('Successfully deleted.')

        return True, new_config

    def github(self, config: Dict[str, str]) -> Tuple[Dict[str, str], Optional[GitHubWorkflow]]:
        """
        Create a GitHub Workflow for the application.
        Workflow is None if the application has been deleted.
        """
        new_config = self.config_loader(GitHubConfig.items, config)
        github_config = GitHubConfig(**new_config)
        workflow = github(self.azure_service, github_config)
        # The deleted configuration is not one we want to propagate.
        new_config.pop('delete', None)
        return new_config, workflow

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
        if not self._web_app:
            raise WebAppNotSetException('The web app must be set before the action.')
        return self._web_app.exists()

    def infrastruture_exists(self) -> bool:
        """
        Return True if the application infrastructure exists, False otherwise.
        """
        if not self._web_app:
            raise WebAppNotSetException('The web app must be set before the action.')
        return self._web_app.resource_group.exists()

    def all(self) -> Iterable['WebApp']:
        """
        Return all WebApp created by WebLodge.
        """
        yield from (
            WebApp(self.config_loader, self.azure_service, web_app)
            for web_app in self.azure_service.all()
        )

    def tiers(self, config: Dict[str, str]) -> List[WebAppTier]:
        """
        Return all tiers of the application.
        """
        new_config = self.config_loader(TiersConfig.items, config)
        tier_config = TiersConfig(**new_config)
        return _tiers(self.azure_service, tier_config)

    def _get_tier(self, config, tier: str) -> WebAppTier:
        """
        Return the tier of the WebApp.
        """
        new_config = self.config_loader(TiersConfig.items, config)
        tier_config = TiersConfig(**new_config)
        tiers = _tiers(self.azure_service, tier_config)

        # Match the tier by name.
        web_app_tier = next((t for t in tiers if t.name.upper() == tier), None)

        # If not found, the tier is invalid.
        if not web_app_tier:
            raise InvalidTier(
                f"Can not find the tier '{tier}' in the location '{tier_config.location}."
            )

        return web_app_tier
