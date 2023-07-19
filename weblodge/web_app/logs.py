"""
Stream logs from an Azure Web App in the user console.
"""
from weblodge.config import Item as ConfigItem
from weblodge._azure import WebApp as AzureWebApp, AppService as AzureAppService, ResourceGroup as AzureResourceGroup


class LogsConfig():
    """
    Logs configuration.

    Azure Web App names are unique across the entire Azure platform. Therefore, simply providing
    the name is enough to retrieve the application logs.
    """
    items = [
        ConfigItem(
            name='subdomain',
            description='The application subdomain.'
        )
    ]

    def __init__(self, subdomain: str, *_args, **_kwargs) -> None:
        self.subdomain = subdomain


def logs(config: LogsConfig):
    """
    Stream logs from the application.
    This function is blocking and never returns.
    User must run CTRL+C to stop the process.
    """
    resource_group = AzureResourceGroup(config.subdomain)

    AzureWebApp(
        config.subdomain,
        resource_group,
        AzureAppService(config.subdomain, resource_group)
    ).logs()
