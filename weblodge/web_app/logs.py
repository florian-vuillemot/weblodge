"""
Stream logs from an Azure Web App in the user console.
"""
from typing import List, Dict

from weblodge.config import Item as ConfigItem
from weblodge._azure import Cli, WebApp


def config() -> List[ConfigItem]:
    """
    Getting logs from the application configuration.
    """
    return [
        ConfigItem(
            name='app_name',
            description='The application name.'
        )
    ]

def logs(config_: Dict[str, str]):
    """
    Stream logs from the application.
    This function is blocking and never returns.
    User must run CTRL+C to stop the process.
    """
    web_app = WebApp(Cli())

    # Stream logs.
    web_app.logs(web_app.get(config_['app_name']))
