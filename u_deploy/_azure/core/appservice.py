from typing import List
from dataclasses import dataclass

from .cli import Cli
from .resource_group import ResourceGroup, ResourceGroupHelper


@dataclass
class AppService:
    id: str
    name: str
    number_of_sites: int
    sku: str
    location: str
    resource_group: ResourceGroup


class AppServiceHelper:
    def __init__(self, cli: Cli) -> None:
        self._cli = cli
        self.appservices = []

    def list(self, force_reload=True) -> List[AppService]:
        """
        List all AppServices Plan.
        """
        if force_reload:
            self.appservices.clear()

        if not self.appservices:
            appservices = self._cli.invoke('appservice plan list')
            for s in appservices:
                a = AppService(
                    id=s['id'],
                    name=s['name'],
                    number_of_sites=int(s['numberOfSites']),
                    sku=s['sku']['name'],
                    resource_group=ResourceGroupHelper(self._cli).get(s['resourceGroup']),
                    location=s['location']
                )
                self.appservices.append(a)

        return self.appservices
    
    def get(self, name: str = None, resource_group: ResourceGroup = None, id_: str = None, force_reload=True) -> AppService:
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

    def delete(self, asp: AppService) -> List[AppService]:
        """
        Delete an AppService Plan.
        """
        self._cli.invoke(f'appservice plan delete --name {asp.name} --resource-group {asp.resource_group.name} --yes', to_json=False)
        return self.list(force_reload=True)

    def create(self, name: str, sku: str, resource_group: ResourceGroup, location: str = None) -> AppService:
        """
        Create a Linux AppService Plan.
        """
        location = location or resource_group.location
        self._cli.invoke(f'appservice plan create --name {name} --sku {sku} --resource-group {resource_group.name} --location {location} --is-linux')
        return self.get(name=name, resource_group=resource_group, force_reload=True)
