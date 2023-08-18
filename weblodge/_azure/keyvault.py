"""
Azure Keyvault interface.
"""
from dataclasses import dataclass
from typing import Dict, Iterable, List

from weblodge._azure.resource_group import ResourceGroup

from .resource import Resource
from .interfaces import AzureKeyVault, AzureKeyVaultSecret
from .exceptions import CLIException, SecretNotFound


@dataclass(frozen=True)
class KeyVaultSecret(AzureKeyVaultSecret):
    """
    Azure KeyVault secret representation.
    """
    # Secret name.
    name: str
    # Secret value.
    value: str
    # Secret URI.
    uri: str


class KeyVault(Resource, AzureKeyVault):
    """
    Azure KeyVault representation.
    It used to store AzureWebApp secrets.
    It is create only if the App Service
    """
    _cli_prefix = 'keyvault'

    def __init__(self, name: str, resource_group: ResourceGroup, from_az: Dict = None) -> None:
        super().__init__(name, from_az)
        self.resource_group = resource_group

    def create(self) -> 'AzureKeyVault':
        """
        Create the Azure KeyVault.
        """
        self._from_az = self._invoke(
            ' '.join([
                'keyvault create',
                f'--location {self.resource_group.location}',
                f'--name {self.name}',
                f'--resource-group {self.resource_group.name}'
            ]),
            tags=self.resource_group.tags
        )

    def delete(self) -> None:
        """
        Delete the resource group.
        """
        self._invoke(
            f'{self._cli_prefix} delete --name {self.name} --yes',
            to_json=False
        )

    def set(self, name: str, value: str) -> KeyVaultSecret:
        """
        Create or update a secret and return its URI.
        """
        secret = self._invoke(
            ' '.join([
                'keyvault secret set',
                f'--vault-name {self.name}',
                f'--name {name}',
                f'--value "{value}"'
            ])
        )
        return KeyVaultSecret(
            uri=secret['id'],
            name=secret['name'],
            value=secret['value']
        )

    def get_all(self) -> Iterable[KeyVaultSecret]:
        """
        Return the KeyVault secrets.
        """
        secrets = self._invoke(f'keyvault secret list --vault-name {self.name}')
        yield from (self._get_secret(s['name']) for s in secrets)

    def _get_secret(self, secret_name: str) -> KeyVaultSecret:
        try:
            secret = self._invoke(
                ' '.join([
                    'az keyvault secret show',
                    f'--vault-name {self.name}',
                    f'--name {secret_name}'
                ])
            )
            return KeyVaultSecret(
                uri=secret['id'],
                name=secret['name'],
                value=secret['value']
            )
        except CLIException as excp:
            raise SecretNotFound(f'Secret "{secret_name}" not found.') from excp

    def _load(self):
        """
        Load the KeyVault from Azure.
        """
        self._from_az.update(
            self._invoke(f'{self._cli_prefix} show --name {self.name}')
        )
        return self
