"""
Azure Web App representation.
"""
from typing import Dict

from .resource import Resource
from .log_level import LogLevel
from .appservice import AppService
from .resource_group import ResourceGroup
from .interfaces import AzureWebApp


class WebApp(Resource, AzureWebApp):
    """
    Azure Web App representation.
    """
    _cli_prefix = 'webapp'

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            name: str,
            resource_group: ResourceGroup,
            app_service: AppService,
            from_az: Dict = None
            ) -> None:
        super().__init__(name=name, from_az=from_az)
        self.python_version = '3.10'
        self.app_service = app_service
        self.resource_group = resource_group

    @property
    def location(self) -> str:
        """
        The WebApp location.
        Ex: northeurope, westeurope, etc.
        """
        return self._from_az['location']

    @property
    def domain(self) -> str:
        """
        WebApp domain.
        """
        return self._from_az['hostNames'][0] if self._from_az['hostNames'] else None

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
        asp = self.app_service.id_
        rg_name = self.resource_group.name
        python_version = self.python_version

        # Create the WebApp infrastructure.
        self._invoke(
            f'{self._cli_prefix} create -g {rg_name} -p {asp} -n {name} --runtime PYTHON:{python_version}',
            tags={**self.resource_group.tags, **self.app_service.tags}
        )
        # Update the WebApp settings.
        self._invoke(
            ' '.join((
                f'{self._cli_prefix} config set --resource-group {rg_name} --name {name}',
                '--web-sockets-enabled true',
                '--http20-enabled',
                '--startup-file weblodge.startup',
                f'--always-on {self.app_service.always_on_supported}',
            ))
        )

    def set_log_level(self, log_level: LogLevel) -> None:
        """
        Update the log level of the WebApp.
        """
        self._invoke(
            ' '.join((
                'webapp log config',
                f'--name {self.name}',
                f'--resource-group {self.resource_group.name}',
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
                f'-g {self.resource_group.name} -n {self.name}',
                f'--src {src}'
            ))
        )

    def logs(self) -> None:
        """
        Stream WebApp logs.
        This is a blocking operation. User must run CTRL+C to stop the process.
        """
        self._invoke(
            f'{self._cli_prefix} log tail -g {self.resource_group.name} -n {self.name}',
            log_outputs=True
        )

    def update_environment(self, env: Dict) -> None:
        """
        Update the WebApp environment variables.
        """
        # Web App App settings format.
        env_formatted = [f'{k}={v}' for k, v in env.items()]

        # Update the WebApp environment variables.
        self._invoke(
            ' '.join((
                f'{self._cli_prefix} config appsettings set',
                f'--name {self.name}',
                f'--resource-group {self.resource_group.name}'
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
                f'--resource-group {self.resource_group.name}'
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
            f'{self._cli_prefix} restart -g {self.resource_group.name} -n {self.name}',
            to_json=False
        )

    @classmethod
    def from_az(cls, name: str, from_az: Dict) -> 'AzureWebApp':
        """
        Create a WebApp from Azure result.
        """
        return cls(
            name,
            ResourceGroup(from_az['resourceGroup']),
            AppService.from_id(from_az['appServicePlanId']),
            from_az=from_az
        )

    def _load(self):
        """
        Load the WebApp from Azure.
        """
        self._from_az.update(
            self._invoke(
                f'{self._cli_prefix} show --resource-group {self.resource_group.name} --name {self.name}'
            )
        )
        return self
