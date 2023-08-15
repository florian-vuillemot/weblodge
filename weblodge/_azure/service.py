"""
Azure Service for Azure instanciation.
"""
from .interfaces import AzureResourceGroup, AzureWebApp, AzureAppService, \
    AzureService, AzureLogLevel, MicrosoftEntra

from .cli import Cli
from .entra import Entra
from .resource_group import ResourceGroup
from .appservice import AppService
from .web_app import WebApp
from .log_level import LogLevel


class Service(AzureService):
    """
    Azure Service.
    Allow to instanciate Azure components.
    """
    resource_groups: AzureResourceGroup
    app_services: AzureAppService
    web_apps: AzureWebApp
    log_levels: AzureLogLevel
    entra: MicrosoftEntra

    def __init__(self):
        self.cli = Cli()

        self.resource_groups: AzureResourceGroup = ResourceGroup
        self.app_services: AzureAppService = AppService
        self.web_apps: AzureWebApp = WebApp
        self.log_levels: AzureLogLevel = LogLevel
        self.entra: MicrosoftEntra = Entra

        self.resource_groups.set_cli(self.cli)
        self.app_services.set_cli(self.cli)
        self.web_apps.set_cli(self.cli)
        self.entra.set_cli(self.cli)
