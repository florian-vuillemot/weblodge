"""
Delete all resources associated with the application.
"""
from weblodge.config import Item as ConfigItem
from weblodge._azure import Cli, ResourceGroup, WebApp


class DeleteConfig:
    """
    Delete configuration.

    Azure Web App names are unique across the entire Azure platform. Therefore, simply providing
    the name is enough to delete the application and all associated resources.
    """
    items = [
        ConfigItem(
            name='app_name',
            description='The application name to delete.'
        )
    ]

    def __init__(self, app_name: str, *_args, **_kwargs) -> None:
        self.app_name = app_name


def delete(config: DeleteConfig) -> None:
    """
    Delete the application and corresponding resources.
    """
    cli = Cli()

    # Retrieve the Azure Web App.
    web_app = WebApp(cli).get(config.app_name)
    # Delete the Azure Web App Resource Group.
    # It is only possible because we are putting all the application resources in the
    # same Resource Group.
    ResourceGroup(cli).delete(web_app.resource_group)
