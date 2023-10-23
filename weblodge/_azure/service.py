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
from .interfaces import AzureWebApp, AzureService, AzureLogLevel, MicrosoftEntra, AzureAppServiceSku


class Service(AzureService):
    """
    Azure Service.
    Allow to instanciate Azure components.
    """
    web_apps: AzureWebApp
    log_levels: AzureLogLevel
    entra: MicrosoftEntra

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

    def entra(self, subdomain: str) -> MicrosoftEntra:
        """
        Return the Entra service.
        """

    def log_levels(self) -> AzureLogLevel:
        """
        Return the log levels.
        """
