from typing import List
from dataclasses import dataclass

from .resource import Resource


@dataclass
class ResourceGroupModel:
    """
    Azure Resource Group representation.
    """
    name: str
    location: str


class ResourceGroup(Resource):
    """
    Helper class to manage Azure Resource Group.
    """
    def list(self, force_reload=False) -> List[ResourceGroupModel]:
        """
        List all Resource Group.
        Force reload clears the cache and reloads the list from Azure.
        """
        if force_reload:
            self._resources.clear()

        if not self._resources:
            rgs = self._cli.invoke('group list')
            for s in rgs:
                a = ResourceGroupModel(
                        name=s['name'],
                        location=s['location']
                )
                self._resources.append(a)

        return self._resources
    
    def get(self, name: str, force_reload=False) -> ResourceGroupModel:
        """
        Return an resource group by its name.
        Force reload clears the cache and reloads the list from Azure.
        """
        for s in self.list(force_reload=force_reload):
            if s.name == name:
                return s

        raise Exception(f"Resource Group '{name}' not found.")

    def create(self, name: str, location: str) -> ResourceGroupModel:
        """
        Create a new Resource Group and return it.
        """
        self._cli.invoke(f'group create --name {name} --location {location}')
        return self.get(name, force_reload=True)

    def delete(self, resource_group: ResourceGroupModel) -> List[ResourceGroupModel]:
        """
        Delete a Resource Group and return all Resource Group.
        """
        self._cli.invoke(f'group delete --name {resource_group.name} --yes', to_json=False)
        return self.list(force_reload=True)
