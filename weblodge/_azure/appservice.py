"""
Azure AppService Plan abstraction.

Allow to CRUD on Azure AppService Plan.
"""
from typing import Dict, Iterable, Optional

from .sku import get_skus, AVAILABLE_SKUS
from .resource import Resource
from .exceptions import InvalidSku
from .resource_group import ResourceGroup
from .interfaces import AzureAppService, AzureAppServiceSku


class AppService(Resource, AzureAppService):
    """
    Azure AppService Plan representation.
    """
    _cli_prefix = 'appservice plan'

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            name: str,
            resource_group: ResourceGroup,
            from_az: Dict = None
        ) -> None:
        super().__init__(name, from_az)
        self.resource_group = resource_group
        self._sku = self._from_az['sku']['name'] if from_az else None

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
        return not self.is_free

    @property
    def is_free(self) -> bool:
        """
        Return True if the AppService Plan is Free.
        """
        if not self._sku:
            self._sku = self._from_az['sku']['name']
        return self._sku == 'F1'

    @property
    def location(self) -> str:
        """
        Return the AppService Plan location.
        """
        return self.resource_group.location

    def set_sku(self, sku_name: str) -> 'AzureAppService':
        """
        Set the AppService Plan SKU.
        """
        if sku_name not in AVAILABLE_SKUS:
            raise InvalidSku(f"Invalid SKU: '{sku_name}'")

        self._sku = sku_name
        return self

    def create(self) -> 'AzureAppService':
        """
        Create a Linux AppService Plan with Python.
        """
        if not self._sku:
            raise InvalidSku('The SKU must be set before creating the AppService Plan.')

        tags = self.resource_group.tags
        rg_name = self.resource_group.name
        location = self.resource_group.location

        self._from_az = self._invoke(
            f'{self._cli_prefix} create --name {self.name} --sku {self._sku} --resource-group {rg_name} --location {location} --is-linux',  # pylint: disable=line-too-long
            tags=tags
        )
        return self

    @classmethod
    def get_existing_free(cls, location: str) -> Optional['AzureAppService']:
        """
        Return the free existing Azure App Service if exists in that location. None otherwise.
        """
        free_asps = filter(lambda asp: asp.is_free, cls.all())
        with_same_location = filter(lambda asp: asp.location == location, free_asps)
        return next(with_same_location, None)

    @staticmethod
    def skus(location: str) -> Iterable[AzureAppServiceSku]:
        """
        Return the list of available SKUs for the given location.
        """
        yield from get_skus(location)

    @classmethod
    def from_id(cls, id_: str) -> 'AzureAppService':
        """
        Return an App Service from an Azure App Service Plan ID.
        """
        from_az = cls._invoke(f'{cls._cli_prefix} show --ids {id_}')
        return cls.from_az(from_az['name'], from_az)

    @classmethod
    def from_az(cls, name: str, from_az: Dict):
        """
        Return an App Service from Azure AppService result.
        """
        return cls(
            name=name,
            resource_group=ResourceGroup(from_az['resourceGroup']),
            from_az=from_az
        )

    def _load(self):
        """
        Load the AppService Plan from Azure.
        """
        self._from_az.update(
            self._invoke(
                f'{self._cli_prefix} show --name {self.name} --resource-group {self.resource_group.name}'
            )
        )
        self._sku = self._from_az['sku']['name']
        return self
