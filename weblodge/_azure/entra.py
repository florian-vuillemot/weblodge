"""
Azure Web App representation.
"""
import json
import os
import tempfile
from .interfaces import MicrosoftEntra, MicrosoftEntraApplication
from .resource_group import ResourceGroup
from .cli import Cli


class EntraApplication(MicrosoftEntraApplication):
    """
    Azure Entra Application with Federated Identity.
    """
    def __init__(self, client_id: str, tenant_id: str, subscription_id: str, cli: Cli) -> None:
        super().__init__()
        self.client_id = client_id
        self.tenant_id = tenant_id
        self.subscription_id = subscription_id

        self._cli = cli

    def delete(self):
        """
        Delete the application.
        """
        self._cli.invoke(f'ad app delete --id {self.client_id}', to_json=False)


class Entra(MicrosoftEntra):
    """
    Azure Entra facade.
    """
    _cli = None

    @classmethod
    def set_cli(cls, cli: Cli):
        """
        Set the Azure CLI.
        """
        cls._cli = cli

    # pylint: disable=too-many-arguments
    @classmethod
    def github_application(
        cls,
        name: str,
        username: str,
        repository: str,
        branch: str,
        resource_group: ResourceGroup
    ) -> EntraApplication:
        """
        Create an GitHub Application on Microsoft Entra.

        :param name: The name of the GitHub Application.
        :param branch: The branch of the repository that will trigger the GitHub Action.
        :param username: The username/organisation of the repository owner.
        :param repository: The name of the GitHub repository.
        :param resource_group: The resource group where the application will be deployed.
        :return: The Microsoft Entra representation.
        """
        name = f'weblodge-{name}'

        # Retrieve need informations.
        account = cls._cli.invoke('account show')
        subscription_id = account['id']
        tenant_id = account['tenantId']

        app_id = cls._get_app_id(name)
        service_principal_id = cls._get_sp_id(name, app_id)
        cls._assign_role(subscription_id, service_principal_id, resource_group)
        cls._create_federated_credential(name, app_id, username, repository, branch)

        return EntraApplication(
            client_id=app_id,
            tenant_id=tenant_id,
            subscription_id=subscription_id,
            cli=cls._cli
        )

    @classmethod
    def _get_app_id(cls, name: str) -> str:
        """
        Retrieve the application ID if the application exists, otherwise create it.
        """
        applications = cls._cli.invoke(f'ad app list --display-name {name}')

        for app in applications:
            if app['displayName'] == name:
                return app['appId']

        return cls._cli.invoke(f'ad app create --display-name {name}')['appId']

    @classmethod
    def _get_sp_id(cls, app_name: str, app_id: str) -> str:
        """
        Retrieve the Service Principal of an Application or create it.
        """
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
