"""
Stream logs from an Azure Web App in the user console.
"""
from weblodge.config import Item as ConfigItem
from weblodge._azure import Cli, WebApp


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


def logs(config: LogsConfig):
    """
    Stream logs from the application.
    This function is blocking and never returns.
    User must run CTRL+C to stop the process.
    """
    web_app = WebApp(Cli())

    # Stream logs.
    web_app.logs(web_app.get(config.app_name))
