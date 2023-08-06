"""
Azure AppService Plan abstraction.

Allow to CRUD on Azure AppService Plan.
"""
from typing import Dict, List

from .cli import Cli
from .resource import Resource
from .resource_group import ResourceGroup
from .exceptions import InvalidSku


class AppService(Resource):
    """
    Azure AppService Plan representation.
    """
    _cli_prefix = 'appservice plan'

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

    @property
    def is_free(self) -> bool:
        """
        Return True if the AppService Plan is Free.
        """
        return self._from_az['sku']['name'] == 'F1'

    @property
    def location(self) -> str:
        """
        Return the AppService Plan location.
        """
        return self.resource_group.location

    def create(self, sku: str) -> 'AppService':
        """
        Create a Linux AppService Plan with Python.
        """
        if sku not in self.sku():
            raise InvalidSku(sku)

        tags = self.resource_group.tags
        rg_name = self.resource_group.name
        location = self.resource_group.location

        self._cli.invoke(
            f'{self._cli_prefix} create --name {self.name} --sku {sku} --resource-group {rg_name} --location {location} --is-linux',  # pylint: disable=line-too-long
            tags=tags
        )
        return self

    @classmethod
    def from_id(cls, id_: str, cli: Cli) -> 'AppService':
        """
        Return an App Service from an Azure App Service Plan ID.
        """
        from_az = cli.invoke(f'{cls._cli_prefix} show --ids {id_}')
        return cls.from_az(from_az['name'], cli, from_az)

    @classmethod
    def from_az(cls, name: str, cli: Cli, from_az: Dict):
        """
        Return an App Service from Azure AppService result.
        """
        return cls(
            name=name,
            resource_group=ResourceGroup(from_az['resourceGroup'], cli),
            cli=cli,
            from_az=from_az
        )

    @staticmethod
    def sku() -> List[str]:
        """
        Return list of supported SKU.
        """
        return [
            'F1', 
            'B1', 'B2', 'B3',
            'P0V3', 'P1MV3', 'P1V2', 'P1V3', 'P2MV3', 'P2V2', 'P2V3', 'P3MV3', 'P3V2', 'P3V3', 'P4MV3', 'P5MV3',
            'S1', 'S2', 'S3'
        ]

    def _load(self):
        """
        Load the AppService Plan from Azure.
        """
        self._from_az.update(
            self._cli.invoke(
                f'{self._cli_prefix} show --name {self.name} --resource-group {self.resource_group.name}'
            )
        )
        return self
