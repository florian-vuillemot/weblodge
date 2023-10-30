"""
Azure Web App representation.
"""
import json
import os
import tempfile
from typing import Optional

from .cli import Cli
from .exceptions import CliNotSet
from .resource_group import ResourceGroup
from .interfaces import MicrosoftEntraApplication


class EntraApplication(MicrosoftEntraApplication):
    """
    Azure Entra Application with Federated Identity.
    """
    def __init__(self, client_id: str, tenant_id: str, subscription_id: str) -> None:
        super().__init__()
        self.client_id = client_id
        self.tenant_id = tenant_id
        self.subscription_id = subscription_id


class Entra:
    """
    Azure Entra facade.
    """
    _cli: Optional[Cli] = None

    @classmethod
    def set_cli(cls, cli: Cli):
        """
        Set the Azure CLI.
        """
        cls._cli = cli

    @classmethod
    def delete_github_application(cls, subdomain: str) -> None:
        """
        Delete an Azure Entra Application for a GitHub Account.

        :param subdomain: The application subdomain of the GitHub Application to delete.
        """
        app_name = cls._to_app_name(subdomain)
        app_id = cls._get_app_id(app_name)
        cls._cli.invoke(f'ad app delete --id {app_id}', to_json=False)

    # pylint: disable=too-many-arguments
    @classmethod
    def get_github_application(
        cls,
        subdomain: str,
        username: str,
        repository: str,
        branch: str,
        location: str
    ) -> EntraApplication:
        """
        Create or return an GitHub Application on Microsoft Entra.

        :param subdomain: The application subdomain of the GitHub Application.
        :param branch: The branch of the repository that will trigger the GitHub Action.
        :param username: The username/organisation of the repository owner.
        :param repository: The name of the GitHub repository.
        :param location: The location of the application.
        :return: The Microsoft Entra representation.
        """
        if not cls._cli:
            raise CliNotSet()

        resource_group = ResourceGroup(name=subdomain, location=location)

        # Permissions are applied on the Resource Group.
        # It must exists.
        if not resource_group.exists():
            resource_group.create()

        app_name = cls._to_app_name(subdomain)

        # Retrieve need informations.
        account = cls._cli.invoke('account show')
        subscription_id = account['id']
        tenant_id = account['tenantId']

        app_id = cls._get_app_id(app_name)
        service_principal_id = cls._get_sp_id(app_name, app_id)
        cls._assign_role(subscription_id, service_principal_id, resource_group)
        cls._create_federated_credential(app_name, app_id, username, repository, branch)

        return EntraApplication(
            client_id=app_id,
            tenant_id=tenant_id,
            subscription_id=subscription_id
        )

    @classmethod
    def _to_app_name(cls, subdomain: str) -> str:
        """
        Convert the public subdomain to an internal GitHub Application name.
        """
        return f'weblodge-{subdomain}'

    @classmethod
    def _get_app_id(cls, name: str) -> str:
        """
        Retrieve the application ID if the application exists, otherwise create it.
        """
        if not cls._cli:
            raise CliNotSet()

        applications = cls._cli.invoke(f'ad app list --display-name {name}')

        for app in applications:
            if app['displayName'] == name:
                return app['appId']

        return cls._cli.invoke(f'ad app create --display-name {name}')['appId']

    @classmethod
    def _get_sp_id(cls, app_name: str, app_id: str) -> str:
        """
        Retrieve/create the Service Principal of an Application.

        Note: Only one Service Principal is created per Application.
        """
        if not cls._cli:
            raise CliNotSet()

        service_principals = cls._cli.invoke(f'ad sp list --display-name {app_name}')

        for service_principal in service_principals:
            if service_principal['appId'] == app_id:
                return service_principal['id']

        return cls._cli.invoke(f'ad sp create --id {app_id}')['id']

    @classmethod
    def _assign_role(cls, subscription_id, service_principal_id, resource_group):
        """
        Assign the owner role to the service principal on the resource group
        if it not already assigned.
        The owner role is required to assign authorizations to KeyVault consumers.
        """
        if not cls._cli:
            raise CliNotSet()

        role_assignments = cls._cli.invoke(
            ' '.join((
                'role assignment list',
                f'--scope {resource_group.id_}',
                f'--assignee {service_principal_id}',
                '--role owner'
            ))
        )
        if role_assignments:
            return

        cls._cli.invoke(
            ' '.join((
                'role assignment create',
                '--role owner',
                f'--subscription {subscription_id}',
                f'--assignee-object-id {service_principal_id}',
                '--assignee-principal-type ServicePrincipal',
                f'--scope {resource_group.id_}'
            )),
            to_json=False
        )

    @classmethod
    def _create_federated_credential(cls, name: str, app_id: str, username: str, repository: str, branch: str):
        """
        Create the federated credential for a GitHub access.
        """
        if not cls._cli:
            raise CliNotSet()

        cred_specs = {
            "name": name,
            "issuer": "https://token.actions.githubusercontent.com",
            "subject": f"repo:{username}/{repository}:ref:refs/heads/{branch}",
            "description": f'WebLodge GitHub Application for application: {name}',
            "audiences": [
                "api://AzureADTokenExchange"
            ]
        }

        creds = cls._cli.invoke(f'ad app federated-credential list --id {app_id}')
        for cred in creds:
            if  cred.get('subject') == cred_specs['subject'] and \
                cred.get('issuer') == cred_specs['issuer'] and \
                cred.get('audiences') == cred_specs['audiences']:
                return

        # pylint: disable=consider-using-with
        credential_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        json.dump(cred_specs, credential_file)
        credential_file.close()

        cls._cli.invoke(
            ' '.join((
                'ad app federated-credential create',
                f'--id {app_id}',
                f'--parameters {credential_file.name}'
            )),
            to_json=False
        )

        os.unlink(credential_file.name)
