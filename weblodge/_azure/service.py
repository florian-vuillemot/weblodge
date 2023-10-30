"""
Azure Service for Azure instanciation.
"""
from typing import Iterable

from .cli import Cli
from .entra import Entra
from .web_app import WebApp
from .keyvault import KeyVault
from .log_level import LogLevel
from .appservice import AppService
from .sku import get_skus as _get_skus
from .resource_group import ResourceGroup
from .interfaces import AzureWebApp, AzureService, AzureLogLevel, MicrosoftEntraApplication, AzureAppServiceSku


class Service(AzureService):
    """
    Azure Service.
    Allow to instanciate Azure components.
    """
    web_apps: AzureWebApp
    log_levels: AzureLogLevel

    def __init__(self):
        self.cli = Cli()

        self.web_apps = WebApp
        self.log_levels = LogLevel
        self.entra = Entra

        self.web_apps.set_cli(self.cli)
        self.entra.set_cli(self.cli)

    def get_web_app(self, subdomain: str) -> AzureWebApp:
        """
        Return a WebApp.
        """
        rg = ResourceGroup(subdomain)
        kv = KeyVault(subdomain, rg)
        app_service = AppService(subdomain, rg)
        return WebApp(subdomain, rg, app_service, kv)

    def get_free_web_app(self, location: str) -> AzureWebApp:
        """
        Return the existing WebApp using a free tier.
        """
        return AppService.get_existing_free(location)

    # pylint: disable=too-many-arguments
    def get_github_application(
        self,
        subdomain: str,
        username: str,
        repository: str,
        branch: str,
        location: str
    ) -> MicrosoftEntraApplication:
        """
        Return a Azure Entra Application for a GitHub Account.
        Create the application if not exists.
        Credentials are federated based.

        :param subdomain: The application subdomain of the GitHub Application
        :param branch: The branch of the repository that will trigger the GitHub Action.
        :param username: The username/organisation of the repository owner.
        :param repository: The name of the GitHub repository.
        :param location: The location of the application.
        :return: The Microsoft Entra representation.
        """
        return self.entra.get_github_application(
            subdomain=subdomain,
            branch=branch,
            username=username,
            repository=repository,
            location=location,
        )

    def delete_github_application(self, subdomain: str) -> None:
        """
        Delete an Azure Entra Application for a GitHub Account.

        :param subdomain: The application subdomain of the GitHub Application to delete.
        """
        self.entra.delete_github_application(subdomain=subdomain)

    def delete(self, subdomain: str) -> None:
        """
        Delete a WebApp.
        """
        ResourceGroup(subdomain).delete()

    def all(self) -> Iterable[AzureWebApp]:
        """
        Return all WebApp created by WebLodge.
        """
        for rg in ResourceGroup.all():
            subdomain = rg.name
            kv = KeyVault(subdomain, rg)
            app_service = AppService(subdomain, rg)
            yield WebApp(subdomain, rg, app_service, kv)

    def get_skus(self, location: str) -> Iterable[AzureAppServiceSku]:
        """
        Return all available tiers.
        """
        return _get_skus(location)

    def log_levels(self) -> AzureLogLevel:
        """
        Return the log levels.
        """
