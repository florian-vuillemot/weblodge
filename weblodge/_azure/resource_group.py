"""
Azure Resource Group interface.
"""
from typing import Dict, Optional

from .resource import Resource


class ResourceGroup(Resource):
    """
    Azure Resource Group representation.
    """
    _cli_prefix = 'group'

    def __init__(
            self,
            name: str,
            location: Optional[str] = None,
            from_az: Optional[Dict] = None
        ) -> None:
        super().__init__(name, from_az)

        if from_az:
            self._location = self._from_az['location']
        else:
            self._location = location

    @property
    def location(self) -> str:
        """
        Return the location.
        """
        if not self._location:
            self._location = self._from_az['location']
        return self._location

    @location.setter
    def location(self, location: str) -> 'ResourceGroup':
        """
        Set the location.
        """
        self._location = location
        return self

    @property
    def id_(self) -> str:
        """
        Return the Resource Group ID.
        """
        return self._from_az['id']

    def create(self, tags: Dict[str, str] = None) -> 'ResourceGroup':
        """
        Create a new Resource Group and return it.
        """
        # Tags are merged with the internal tags.
        tags = {
            **(tags or {}),
            **self._internal_tags
        }

        self._from_az.update(
            self._invoke(
                f'{self._cli_prefix} create --name {self.name} --location {self.location}',
                tags=tags
            )
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
        return cls(name=name, from_az=from_az)

    def _load(self):
        """
        Load the Resource Group from Azure.
        """
        self._from_az.update(
            self._invoke(f'{self._cli_prefix} show --name {self.name}')
        )
        return self
