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

    def list(self) -> list[AppService]:
        """
        List all AppServices Plan.
        """
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
    
    def get(self, name: str = None, resource_group: ResourceGroup = None, id_: str = None) -> AppService:
        """
        Return an appservice by its name or its id.
        If resource_group is provided, it will used with the name based search.
        """
        for s in self.list():
            if s.id == id_:
                return s
            if s.name == name:
                if resource_group is None or s.resource_group.name == resource_group.name:
                    return s

        raise Exception(f"AppService '{name}' not found.")

    def create(self, name: str, sku: str, location: str, resource_group: ResourceGroup) -> AppService:
        """
        Create a new AppService Plan.
        """
        self._cli.invoke(f'appservice plan create --name {name} --sku {sku} --resource-group {resource_group.name} --location {location}')
