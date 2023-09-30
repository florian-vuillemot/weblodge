"""
Azure Service for Azure instanciation.
"""
from .interfaces import AzureResourceGroup, AzureWebApp, AzureAppService, \
    AzureService, AzureLogLevel, MicrosoftEntra, AzureKeyVault

from .cli import Cli
from .entra import Entra
from .web_app import WebApp
from .keyvault import KeyVault
from .log_level import LogLevel
from .appservice import AppService
from .resource_group import ResourceGroup


class Service(AzureService):
    """
    Azure Service.
    Allow to instanciate Azure components.
    """
    resource_groups: AzureResourceGroup
    app_services: AzureAppService
    web_apps: AzureWebApp
    log_levels: AzureLogLevel
    keyvaults: AzureKeyVault
    entra: MicrosoftEntra

    def __init__(self):
        self.cli = Cli()

        self.resource_groups: AzureResourceGroup = ResourceGroup
        self.app_services: AzureAppService = AppService
        self.web_apps: AzureWebApp = WebApp
        self.log_levels: AzureLogLevel = LogLevel
        self.keyvaults: AzureKeyVault = KeyVault
        self.entra: MicrosoftEntra = Entra

        self.resource_groups.set_cli(self.cli)
        self.app_services.set_cli(self.cli)
        self.web_apps.set_cli(self.cli)
        self.keyvaults.set_cli(self.cli)
        self.entra.set_cli(self.cli)
