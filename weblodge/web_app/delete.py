"""
Delete all resources associated with the application.
"""
from typing import List
from dataclasses import dataclass

from weblodge.config import Item as ConfigItem
from weblodge._azure import Cli, ResourceGroup, WebApp


@dataclass
class Delete:
    """
    Facade to the delete process.

    Azure Web App names are unique across the entire Azure platform. Therefore, simply providing
    the name is enough to delete the application and all associated resources.
    """
    # Application name to delete.
    app_name: str = None

    @classmethod
    def config(cls) -> List[ConfigItem]:
        """
        Delete class configuration.
        """
        return [
            ConfigItem(
                name='app_name',
                description='The application name to delete.',
                default=cls.app_name
            )
        ]

    def delete(self) -> None:
        """
        Delete the application and corresponding resources.
        """
        cli = Cli()

        # Retrieve the Azure Web App.
        web_app = WebApp(cli).get(self.app_name)
        # Delete the Azure Web App Resource Group.
        # It is only possible because we are putting all the application resources in the
        # same Resource Group.
        ResourceGroup(cli).delete(web_app.resource_group)
