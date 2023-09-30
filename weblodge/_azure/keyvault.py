"""
Azure Keyvault interface.
"""
from dataclasses import dataclass
from typing import Dict, Iterable

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

    @property
    def id_(self) -> str:
        """
        Return the KeyVault ID.
        """
        return self._from_az['id']

    def create(self) -> 'AzureKeyVault':
        """
        Create the Azure KeyVault and set the current user as Secret Officer.
        """
        self._from_az = self._invoke(
            ' '.join([
                f'{self._cli_prefix} create',
                f'--location {self.resource_group.location}',
                f'--name {self.name}',
                f'--resource-group {self.resource_group.name}',
                '--enable-rbac-authorization true',
                '--retention-days 7',
            ]),
            tags=self.resource_group.tags
        )
        # Set the current user as Secret Officer.
        self._invoke(
            ' '.join((
                'role assignment create',
                f'--assignee {self._user_id}',
                f'--scope {self.id_}',
            )),
            to_json=False,
            command_args=['--role', 'Key Vault Secrets Officer']
        )
        return self

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
                f'{self._cli_prefix} secret set',
                f'--vault-name {self.name}',
                f'--name {name}'
            ]),
            command_args=['--value', value]
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
        secrets = self._invoke(f'{self._cli_prefix} secret list --vault-name {self.name}')
        yield from (self._get_secret(s['name']) for s in secrets)

    def can_read_secrets(self, identity: str) -> None:
        """
        Add read permission on the KeyVault secrets.
        """
        self._invoke(
            ' '.join((
                'role assignment create',
                f'--assignee {identity}',
                f'--scope {self.id_}',
            )),
            to_json=False,
            command_args=['--role', 'Key Vault Secrets User']
        )

    @classmethod
    def from_az(cls, name: str, from_az: Dict):
        """
        Create a resource from Azure.
        """
        return cls(
            name=name,
            resource_group=ResourceGroup(from_az['resourceGroup']),
            from_az=from_az
        )

    def _get_secret(self, secret_name: str) -> KeyVaultSecret:
        try:
            secret = self._invoke(
                ' '.join([
                    f'{self._cli_prefix} secret show',
                    f'--vault-name {self.name}',
                    f'--name {secret_name}',
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
