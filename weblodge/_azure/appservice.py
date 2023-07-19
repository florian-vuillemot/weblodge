"""
Azure AppService Plan abstraction.

Allow to CRUD on Azure AppService Plan.
"""
from typing import Dict

from weblodge._azure.cli import Cli

from .cli import Cli
from .resource import Resource
from .resource_group import ResourceGroup


class AppService(Resource):
    """
    Azure AppService Plan representation.
    """
    # pylint: disable=too-many-arguments
    def __init__(
            self,
            name: str,
            resource_group: ResourceGroup,
            cli: Cli = Cli(),
            from_az: Dict = None
        ) -> None:
        super().__init__(name, cli, from_az)
        self.resource_group = resource_group

    @property
    def id_(self) -> str:
        """
        Return the AppService Plan ID.
        """
        return self._from_az['id']

    @property
    def always_on_supported(self) -> bool:
        """
        Return True if the AppService Plan support AlwaysOn.
        """
        return self._from_az['sku']['name'] != 'F1'

    def create(self, sku: str) -> 'AppService':
        """
        Create a Linux AppService Plan with Python.
        """
        tags = self.resource_group.tags
        rg_name = self.resource_group.name
        location = self.resource_group.location

        self._from_az = self._cli.invoke(
            f'appservice plan create --name {self.name} --sku {sku} --resource-group {rg_name} --location {location} --is-linux',  # pylint: disable=line-too-long
            tags=tags
        )
        return self

    def _load(self):
        """
        Load the AppService Plan from Azure.
        """
        self._from_az.update(
            self._cli.invoke(
                f'appservice plan show --name {self.name} --resource-group {self.resource_group.name}'
            )
        )
        return self
