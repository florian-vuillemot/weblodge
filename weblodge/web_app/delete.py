"""
Delete all resources associated with the application.
"""
from weblodge._azure import ResourceGroup
from weblodge.config import Item as ConfigItem


class DeleteConfig:
    """
    Delete configuration.

    Azure Web App names are unique across the entire Azure platform. Therefore, simply providing
    the name is enough to delete the application and all associated resources.
    """
    items = [
        ConfigItem(
            name='subdomain',
            description='The application name to delete.'
        )
    ]

    def __init__(self, subdomain: str, *_args, **_kwargs) -> None:
        self.subdomain = subdomain


def delete(config: DeleteConfig) -> None:
    """
    Delete the application and corresponding resources.
    """
    ResourceGroup(config.subdomain).delete()
