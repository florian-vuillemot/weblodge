"""

"""
from pathlib import Path

from weblodge.config import Item as ConfigItem
from weblodge._azure import MicrosoftEntraApplication, AzureService

from .build import BuildConfig
from .deploy import DeploymentConfig


class GitHubConfig:
    """
    """
    # Configurable items of the build.
    items = [
        ConfigItem(
            name='branch',
            description='The deployment branch.',
            default='main'
        ),
        ConfigItem(
            name='username',
            description='The GitHub username.',
            default='main'
        ),
        ConfigItem(
            name='repository',
            description='The GitHub repository.',
            default='main'
        ),
        *BuildConfig.items,
        *DeploymentConfig.items
    ]

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        subdomain: str,
        branch: str,
        username: str,
        repository: str,
        *_args,
        **_kwargs
    ):
        self.subdomain = subdomain
        self.branch = branch
        self.username = username
        self.repository = repository


def github(service: AzureService, config: GitHubConfig) -> MicrosoftEntraApplication:
    """
    """
    return service.entra.github_application(
        name=config.subdomain,
        branch=config.branch,
        username=config.username,
        repository=config.repository,
        resource_group=config.subdomain
    )
