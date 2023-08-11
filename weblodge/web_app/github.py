"""
GitHub Application on Microsoft Entra.
It allows to deploy an application on Azure WebApplication using GitHub Actions.
"""
from weblodge.config import Item as ConfigItem
from weblodge._azure import MicrosoftEntraApplication, AzureService

from .build import BuildConfig
from .deploy import DeploymentConfig


class GitHubConfig:
    """
    GitHub Application configuration.
    Handle deployment and build configuration.
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
        location: str,
        *_args,
        **_kwargs
    ):
        self.subdomain = subdomain
        self.branch = branch
        self.username = username
        self.repository = repository
        self.location = location


def github(service: AzureService, config: GitHubConfig) -> MicrosoftEntraApplication:
    """
    Create a GitHub Application on Microsoft Entra.
    """
    resource_group = service.resource_groups(config.subdomain)

    if not resource_group.exists():
        resource_group.create(config.location)

    return service.entra.github_application(
        name=config.subdomain,
        branch=config.branch,
        username=config.username,
        repository=config.repository,
        resource_group=resource_group
    )
