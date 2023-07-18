"""
Stream logs from an Azure Web App in the user console.
"""
from weblodge._azure import WebApp as AzureWebApp, AppService as AzureAppService, ResourceGroup as AzureResourceGroup
from weblodge.config import Item as ConfigItem


class LogsConfig():
    """
    Logs configuration.

    Azure Web App names are unique across the entire Azure platform. Therefore, simply providing
    the name is enough to retrieve the application logs.
    """
    items = [
        ConfigItem(
            name='app_name',
            description='The application name.'
        )
    ]

    def __init__(self, app_name: str, *_args, **_kwargs) -> None:
        self.app_name = app_name


def logs(config: LogsConfig):
    """
    Stream logs from the application.
    This function is blocking and never returns.
    User must run CTRL+C to stop the process.
    """
    AzureWebApp(
        config.app_name,
        AzureResourceGroup(config.app_name),
        AzureAppService(config.app_name)
    ).logs()
