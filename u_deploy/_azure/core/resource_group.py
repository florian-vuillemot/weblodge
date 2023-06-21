from typing import List
from dataclasses import dataclass

from .cli import Cli


@dataclass
class ResourceGroup:
    name: str
    location: str


class ResourceGroupHelper:
    def __init__(self, cli: Cli) -> None:
        self._cli = cli
        self.resource_groups = []

    def list(self, force_reload=False) -> List[ResourceGroup]:
        """
        List all Resource Group.
        Force reload clears the cache and reloads the list from Azure.
        """
        if force_reload:
            self.resource_groups.clear()

        if not self.resource_groups:
            rgs = self._cli.invoke('group list')
            for s in rgs:
                a = ResourceGroup(
                        name=s['name'],
                        location=s['location']
                )
                self.resource_groups.append(a)

        return self.resource_groups
    
    def get(self, name: str, force_reload=False) -> ResourceGroup:
        """
        Return an resource group by its name.
        Force reload clears the cache and reloads the list from Azure.
        """
        for s in self.list(force_reload=force_reload):
            if s.name == name:
                return s

        raise Exception(f"Resource Group '{name}' not found.")

    def create(self, name: str, location: str) -> ResourceGroup:
        """
        Create a new Resource Group and return it.
        """
        self._cli.invoke(f'group create --name {name} --location {location}')
        return self.get(name, force_reload=True)

    def delete(self, name: str) -> List[ResourceGroup]:
        """
        Delete a Resource Group and return all Resource Group.
        """
        self._cli.invoke(f'group delete --name {name} --yes')
        return self.list(force_reload=True)
