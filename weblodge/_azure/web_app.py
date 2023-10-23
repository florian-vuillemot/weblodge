"""
Azure Web App representation.
"""
from typing import Dict, Optional

from .resource import Resource
from .appservice import AppService
from .resource_group import ResourceGroup
from .keyvault import KeyVault
from .interfaces import AzureWebApp, AzureLogLevel
from .exceptions import CanNotChangeTheResourceLocation


class WebApp(Resource, AzureWebApp):
    """
    Azure Web App representation.
    """
    _cli_prefix: str = 'webapp'

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            name: str,
            resource_group: ResourceGroup,
            app_service: AppService,
            keyvault: KeyVault,
            from_az: Optional[Dict] = None
        ) -> None:
        super().__init__(name=name, from_az=from_az)
        self.python_version = '3.10'
        self._app_service = app_service
        self._resource_group = resource_group
        self._keyvault = keyvault

    @property
    def tier(self) -> AzureWebApp:
        """
        Return the WebApp tier.
        """
        return self._app_service.sku

    @tier.setter
    def tier(self, tier_name: str):
        """
        Set the WebApp tier.
        """
        self._app_service.sku = tier_name

    @property
    def location(self) -> str:
        """
        The WebApp location.
        Ex: northeurope, westeurope, etc.
        """
        return self._resource_group.location

    @location.setter
    def location(self, location) -> 'WebApp':
        """
        The WebApp location.
        Ex: northeurope, westeurope, etc.
        """
        if self.exists():
            raise CanNotChangeTheResourceLocation('Cannot change location of an existing WebApp')

        self._resource_group.location = location
        return self

    @property
    def domain(self) -> str:
        """
        WebApp domain.
        """
        return self._from_az['hostNames'][0] if self._from_az['hostNames'] else None

    def is_free(self) -> bool:
        """
        Return True if the WebApp is Free.
        """
        return self._app_service.is_free

    def create(self) -> 'AzureWebApp':
        """
        Create the WebApp infrastructure.

        Settings enabled:
        - WebSockets
        - HTTP/2
        - Always On: If the SKU is not F1.
        - Startup file: weblodge.startup
        """
        name = self.name
        rg_name = self._resource_group.name
        python_version = self.python_version

        if not self._resource_group.exists():
            self._resource_group.create()

        if not self._app_service.exists():
            self._app_service.create()
        asp = self._app_service.id_

        if not self._keyvault.exists():
            self._keyvault.create()

        # Create the WebApp infrastructure.
        self._invoke(
            f'{self._cli_prefix} create -g {rg_name} -p {asp} -n {name} --runtime PYTHON:{python_version}',
            tags=self.tags
        )
        # Update the WebApp settings.
        self._invoke(
            ' '.join((
                f'{self._cli_prefix} config set --resource-group {rg_name} --name {name}',
                '--web-sockets-enabled true',
                '--http20-enabled',
                '--startup-file weblodge.startup',
                f'--always-on {self._app_service.always_on_supported}',
            ))
        )
        # Retrieve the WebApp identity.
        identity = self._invoke(
            ' '.join((
                f'{self._cli_prefix} identity assign',
                f'-g {self._resource_group.name}',
                f'-n {self.name}',
            ))
        )
        # Allow the WebApp to read the KeyVault secrets.
        self._keyvault.can_read_secrets(identity['principalId'])
        return self

    def set_log_level(self, log_level: AzureLogLevel) -> None:
        """
        Update the log level of the WebApp.
        """
        self._invoke(
            ' '.join((
                f'{self._cli_prefix} log config',
                f'--name {self.name}',
                f'--resource-group {self._resource_group.name}',
                '--application-logging filesystem',
                '--docker-container-logging filesystem',
                '--detailed-error-messages true',
                '--failed-request-tracing true',
                f'--level {log_level.to_azure()}'
            ))
        )

    def deploy(self, src: str) -> None:
        """
        Deploy an application zipped.
        """
        self._invoke(
            ' '.join((
                f'{self._cli_prefix} deployment source config-zip',
                f'-g {self._resource_group.name} -n {self.name}',
                f'--src {src}'
            ))
        )

    def logs(self) -> None:
        """
        Stream WebApp logs.
        This is a blocking operation. User must run CTRL+C to stop the process.
        """
        self._invoke(
            f'{self._cli_prefix} log tail -g {self._resource_group.name} -n {self.name}',
            log_outputs=True
        )

    def update_environment(self, env: Dict) -> None:
        """
        Update the WebApp environment variables.
        """
        env_formatted = []

        # Insert secret in KeyVault.
        for name, value in env.items():
            secret = self._keyvault.set(name, value)
            env_formatted.append(f'{name}=@Microsoft.KeyVault(SecretUri={secret.uri})')

        # Update the WebApp environment variables.
        self._invoke(
            ' '.join((
                f'{self._cli_prefix} config appsettings set',
                f'--name {self.name}',
                f'--resource-group {self._resource_group.name}'
            )),
            to_json=False,
            # Provide as independent arguments to avoid shell escaping issues.
            command_args=['--settings', *env_formatted]
        )

    def deployment_in_progress(self) -> bool:
        """
        True if the WebApp is deploying.
        """
        deployments = self._invoke(
            ' '.join((
                f'{self._cli_prefix} log deployment show',
                f'--name {self.name}',
                f'--resource-group {self._resource_group.name}'
            ))
        )
        return any(
            'Deployment successful' in d.get('message')
            for d in deployments
        )

    def restart(self) -> None:
        """
        Restart the WebApp.
        """
        self._invoke(
            f'{self._cli_prefix} restart -g {self._resource_group.name} -n {self.name}',
            to_json=False
        )

    def update(self) -> 'WebApp':
        """
        Update the WebApp infrastructure.
        """
        super().update()
        self._resource_group.update()
        self._app_service.update()
        return self

    @classmethod
    def from_az(cls, name: str, from_az: Dict) -> 'AzureWebApp':
        """
        Create a WebApp from Azure result.
        """
        resource_group = ResourceGroup(from_az['resourceGroup'])
        return cls(
            name=name,
            resource_group=resource_group,
            app_service=AppService.from_id(from_az['appServicePlanId']),
            keyvault=KeyVault(name=name, resource_group=resource_group),
            from_az=from_az
        )

    def _load(self):
        """
        Load the WebApp from Azure.
        """
        self._from_az.update(
            self._invoke(
                f'{self._cli_prefix} show --resource-group {self._resource_group.name} --name {self.name}'
            )
        )
        return self
