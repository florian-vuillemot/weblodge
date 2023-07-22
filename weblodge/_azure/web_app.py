"""
Azure Web App representation.
"""
from typing import Dict


from .cli import Cli
from .resource import Resource
from .resource_group import ResourceGroup
from .appservice import AppService


class WebAppNotfound(Exception):
    """
    Exception raised when a WebApp is not found.
    """


class WebApp(Resource):
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
            cli: Cli = Cli(),
            from_az: Dict = None
            ) -> None:
        super().__init__(name=name, cli=cli, from_az=from_az)
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

    def create(self) -> 'WebApp':
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
        self._cli.invoke(
            f'{self._cli_prefix} create -g {rg_name} -p {asp} -n {name} --runtime PYTHON:{python_version}',
            tags={**self.resource_group.tags, **self.app_service.tags}
        )
        # Update the WebApp settings.
        self._cli.invoke(
            ' '.join((
                f'{self._cli_prefix} config set --resource-group {rg_name} --name {name}',
                '--web-sockets-enabled true',
                '--http20-enabled',
                '--startup-file weblodge.startup',
                f'--always-on {self.app_service.always_on_supported}',
            ))
        )

    def deploy(self, src: str) -> None:
        """
        Deploy an application zipped.
        """
        self._cli.invoke(
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
        self._cli.invoke(
            f'{self._cli_prefix} log tail -g {self.resource_group.name} -n {self.name}',
            log_outputs=True
        )

    @classmethod
    def from_az(cls, name: str, cli: Cli, from_az: Dict) -> 'WebApp':
        """
        Create a WebApp from Azure result.
        """
        return cls(
            name,
            ResourceGroup(from_az['resourceGroup'], cli=cli),
            AppService.from_id(from_az['appServicePlanId'], cli=cli),
            cli=cli,
            from_az=from_az
        )

    def _load(self):
        """
        Load the WebApp from Azure.
        """
        self._from_az.update(
            self._cli.invoke(
                f'{self._cli_prefix} show --resource-group {self.resource_group.name} --name {self.name}'
            )
        )
        return self
