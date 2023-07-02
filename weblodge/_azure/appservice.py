from typing import Dict, List
from dataclasses import dataclass

from .cli import Cli
from .resource_group import ResourceGroupModel, ResourceGroup


@dataclass(frozen=True)
class AppServiceModel:
    """
    Azure AppService Plan representation.
    """
    id: str
    name: str
    number_of_sites: int
    sku: str
    location: str
    resource_group: ResourceGroupModel
    tags: Dict[str, str]


class AppService:
    """
    Helper class to manage Azure AppServices Plan.
    """
    def __init__(self, cli: Cli()) -> None:
        self._cli = cli
        self._resources = []

    def list(self, force_reload=False) -> List[AppServiceModel]:
        """
        List all AppServices Plan.
        """
        if force_reload:
            self._resources.clear()

        if not self._resources:
            appservices = self._cli.invoke('appservice plan list')
            for s in appservices:
                a = AppServiceModel(
                    id=s['id'],
                    name=s['name'],
                    number_of_sites=int(s['numberOfSites']),
                    sku=s['sku']['name'],
                    resource_group=ResourceGroup(self._cli).get(s['resourceGroup']),
                    location=s['location'],
                    tags=s['tags']
                )
                self._resources.append(a)

        return self._resources
    
    def get(self, name: str = None, resource_group: ResourceGroupModel = None, id_: str = None, force_reload=True) -> AppServiceModel:
        """
        Return an appservice by its name or its id.
        If resource_group is provided, it will used with the name based search.
        """
        for s in self.list(force_reload=force_reload):
            if s.id == id_:
                return s
            if s.name == name:
                if resource_group is None or s.resource_group.name == resource_group.name:
                    return s

        raise Exception(f"AppService '{name}' not found.")

    def delete(self, asp: AppServiceModel) -> List[AppServiceModel]:
        """
        Delete an AppService Plan.
        """
        self._cli.invoke(f'appservice plan delete --name {asp.name} --resource-group {asp.resource_group.name} --yes', to_json=False)
        return self.list(force_reload=True)

    def create(self, name: str, sku: str, resource_group: ResourceGroupModel, location: str = None, tags: Dict[str, str] = {}) -> AppServiceModel:
        """
        Create a Linux AppService Plan.
        """
        location = location or resource_group.location
        self._cli.invoke(f'appservice plan create --name {name} --sku {sku} --resource-group {resource_group.name} --location {location} --is-linux', tags=tags)
        return self.get(name=name, resource_group=resource_group, force_reload=True)
