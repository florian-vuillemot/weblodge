"""
Azure Resource Group interface.
"""
from typing import Dict, List
from dataclasses import dataclass

from .cli import Cli


@dataclass(frozen=True)
class ResourceGroupModel:
    """
    Azure Resource Group representation.
    """
    name: str
    location: str
    tags: Dict[str, str]


class ResourceGroup:
    """
    Helper class to manage Azure Resource Group.
    """
    def __init__(self, cli: Cli()) -> None:
        self._cli = cli
        self._resources = []

    def list(self, force_reload=False) -> List[ResourceGroupModel]:
        """
        List all Resource Group.
        Force reload clears the cache and reloads the list from Azure.
        """
        if force_reload:
            self._resources.clear()

        if not self._resources:
            for group in self._cli.invoke('group list'):
                self._resources.append(
                    ResourceGroupModel(
                        name=group['name'],
                        location=group['location'],
                        tags=group['tags']
                    )
                )

        return self._resources

    def get(self, name: str, force_reload=False) -> ResourceGroupModel:
        """
        Return an resource group by its name.
        Force reload clears the cache and reloads the list from Azure.
        """
        for group in self.list(force_reload=force_reload):
            if group.name == name:
                return group

        raise Exception(f"Resource Group '{name}' not found.")  # pylint: disable=broad-exception-raised

    def create(self, name: str, location: str, tags: Dict[str, str] = None) -> ResourceGroupModel:
        """
        Create a new Resource Group and return it.
        """
        tags = tags or {}

        self._cli.invoke(f'group create --name {name} --location {location}', tags=tags)
        return self.get(name, force_reload=True)

    def delete(self, resource_group: ResourceGroupModel) -> List[ResourceGroupModel]:
        """
        Delete a Resource Group and return all Resource Group.
        """
        self._cli.invoke(f'group delete --name {resource_group.name} --yes', to_json=False)
        return self.list(force_reload=True)
