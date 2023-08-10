"""
Azure Web App representation.
"""
import json
import tempfile
from .interfaces import MicrosoftEntra, MicrosoftEntraApplication
from .cli import Cli


class EntraApplication(MicrosoftEntraApplication):
    """
    Azure Entra Application with Federated Identity.
    """
    def __init__(self, client_id: str, tenant_id: str, subscription_id: str) -> None:
        super().__init__()
        self.client_id = client_id
        self.tenant_id = tenant_id
        self.subscription_id = subscription_id


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
    def github_application(
        self,
        name: str,
        username: str,
        repository: str,
        branch: str,
        resource_group: str
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
        account = self._cli.invoke('account show')
        subscription_id = account['id']
        tenant_id = account['tenantId']
        resource_group = f'/subscriptions/{subscription_id}/resourceGroups/{resource_group}'

        # Create the application.
        app = self._cli.invoke(f'ad app create --display-name {name}')
        # Create the service principal.
        service_principal = self._cli.invoke(f'ad sp create --id {app["appId"]}')
        # Assign the contributor role to the service principal on the resource group.
        self._cli.invoke(
            ' '.join((
                'az role assignment create',
                '--role contributor',
                f'--subscription {subscription_id}',
                f'--assignee-object-id {service_principal["id"]}',
                '--assignee-principal-type ServicePrincipal',
                f'--scope {resource_group}'
            ))
        )

        # Create the federated credential.
        with tempfile.NamedTemporaryFile(mode='w') as credential_file:
            credential_file.write(
                json.dumps(
                    {
                        "name": name,
                        "issuer": "https://token.actions.githubusercontent.com",
                        "subject": f"repo:{username}/{repository}:ref:{branch}",
                        "description": f'WebLodge GitHub Application for application: {name}',
                        "audiences": [
                            "api://AzureADTokenExchange"
                        ]
                    }
                )
            )
            self._cli.invoke(
                ' '.join((
                    'az ad app federated-credential create',
                    f'--id {app["appId"]}',
                    f'--parameters {credential_file.name}'
                ))
            )

        return EntraApplication(
            client_id=app["appId"],
            tenant_id=tenant_id,
            subscription_id=subscription_id
        )
