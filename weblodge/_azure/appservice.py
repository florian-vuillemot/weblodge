"""
Azure AppService Plan abstraction.

Allow to CRUD on Azure AppService Plan.
"""
from typing import Dict, List
from dataclasses import dataclass

from .cli import Cli
from .resource_group import ResourceGroupModel, ResourceGroup


@dataclass(frozen=True)
class AppServiceModel:
    """
    Azure AppService Plan representation.
    """
    id: str  # pylint: disable=invalid-name
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
            for asp in appservices:
                self._resources.append(
                    AppServiceModel(
                        id=asp['id'],
                        name=asp['name'],
                        number_of_sites=int(asp['numberOfSites']),
                        sku=asp['sku']['name'],
                        resource_group=ResourceGroup(self._cli).get(asp['resourceGroup']),
                        location=asp['location'],
                        tags=asp['tags']
                    )
                )

        return self._resources

    def get(
            self,
            name: str = None,
            resource_group: ResourceGroupModel = None,
            id_: str = None,
            force_reload: bool = False
        ) -> AppServiceModel:
        """
        Return an appservice by its name or its id.
        If resource_group is provided, it will used with the name based search.
        """
        for asp in self.list(force_reload=force_reload):
            if asp.id == id_:
                return asp
            if asp.name == name:
                if resource_group is None or asp.resource_group.name == resource_group.name:
                    return asp

        raise Exception(f"AppService name='{name}', id='{id_}' not found.")  # pylint: disable=broad-exception-raised

    def delete(self, asp: AppServiceModel) -> List[AppServiceModel]:
        """
        Delete an AppService Plan.
        """
        asp_name = asp.name
        rg_name = asp.resource_group.name

        self._cli.invoke(
            f'appservice plan delete --name {asp_name} --resource-group {rg_name} --yes',
            to_json=False
        )

        return self.list(force_reload=True)

    # pylint: disable=too-many-arguments
    def create(
            self,
            name: str,
            sku: str,
            resource_group: ResourceGroupModel,
            location: str = None,
            tags: Dict[str, str] = None
        ) -> AppServiceModel:
        """
        Create a Linux AppService Plan.
        """
        tags = tags or resource_group.tags
        location = location or resource_group.location

        self._cli.invoke(
            f'appservice plan create --name {name} --sku {sku} --resource-group {resource_group.name} --location {location} --is-linux',  # pylint: disable=line-too-long
            tags=tags
        )

        return self.get(name=name, resource_group=resource_group, force_reload=True)
