"""
Azure Resource Group interface.
"""
from typing import Dict

from .resource import Resource
from .interfaces import AzureResourceGroup


class ResourceGroup(Resource, AzureResourceGroup):
    """
    Azure Resource Group representation.
    """
    _cli_prefix = 'group'

    @property
    def id_(self) -> str:
        """
        Return the Resource Group ID.
        """
        return self._from_az['id']

    @property
    def location(self) -> str:
        """
        Return the Resource Group location.
        """
        return self._from_az['location']

    def create(self, location: str, tags: Dict[str, str] = None) -> 'ResourceGroup':
        """
        Create a new Resource Group and return it.
        """
        # Tags are merged with the internal tags.
        tags = {
            **(tags or {}),
            **self._internal_tags
        }

        self._invoke(
            f'{self._cli_prefix} create --name {self.name} --location {location}',
            tags=tags
        )
        return self

    def delete(self) -> None:
        """
        Delete the resource group.
        """
        self._invoke(f'{self._cli_prefix} delete --name {self.name} --yes', to_json=False)

    @classmethod
    def from_az(cls, name: str, from_az: Dict):
        """
        Create the Resource Group from Azure.
        """
        return cls(name, from_az)

    def _load(self):
        """
        Load the Resource Group from Azure.
        """
        self._from_az.update(
            self._invoke(f'{self._cli_prefix} show --name {self.name}')
        )
        return self
