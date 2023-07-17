"""
Azure Web App representation.
"""
from typing import List, Dict

from .cli import Cli
from .resource_group import ResourceGroupModel, ResourceGroup
from .appservice import AppServiceModel, AppService


class WebAppNotfound(Exception):
    """
    Exception raised when a WebApp is not found.
    """


class WebApp:
    """
    Azure Web App representation.
    """
    _resources = []

    def __init__(self, name: str, cli: Cli = Cli(), from_az: Dict = None) -> None:
        self.cli = cli
        self.name = name
        self.python_version = '3.10'

        # Azure representation.
        self._from_az = from_az or {}

        self._asp = None
        self._rg = None

    def __eq__(self, other: object) -> bool:
        return other.name == self.name

    @property
    def kind(self) -> str:
        return self._from_az['kind']

    @property
    def location(self) -> str:
        return self._from_az['location']

    @property
    def linux_fx_version(self) -> str:
        return self._from_az['siteConfig']['linuxFxVersion']

    @property
    def tags(self) -> Dict[str, str]:
        return self._from_az['tags']

    @property
    def domain(self) -> str:
        return self._from_az['hostNames'][0] if self._from_az['hostNames'] else None

    @property
    def app_service(self) -> AppServiceModel:
        if not self._asp:
            self._asp = AppService(self.cli).get(
                id_=self._from_az['appServicePlanId'],
            )
        return self._asp

    @property
    def resource_group(self) -> ResourceGroupModel:
        if not self._rg:
            self._rg = ResourceGroup(self.cli).get(
                self._from_az['resourceGroup']
            )
        return self._rg

    @classmethod
    def all(cls, cli: Cli = Cli(), force_reload: bool = False) -> List['WebApp']:
        """
        List all WebApps.
        """
        if not cls._resources or force_reload:
            web_apps = cli.invoke('webapp list')
            cls._resources = [cls(web_app['name'], cli, web_app) for web_app in web_apps]
        return cls._resources

    def load(self, force_reload: bool = False, retry: int = 1) -> 'WebApp':
        """
        Load the WebApp from Azure.
        """
        for i in self.all(force_reload=force_reload):
            if i == self:
                self._from_az = i._from_az
                return self
        if retry:
            return self.load(force_reload=True, retry=retry - 1)
        raise WebAppNotfound(f'WebApp {self.name} not found.')

    def exists(self) -> bool:
        return bool(next((web_app for web_app in self.all() if web_app == self), False))

    def create(self, app_service: AppServiceModel, resource_group: ResourceGroupModel) -> 'WebApp':
        """
        Create the WebApp infrastructure.

        Settings enabled:
        - WebSockets
        - HTTP/2
        - Always On: If the SKU is not F1.
        - Startup file: weblodge.startup
        """
        name = self.name
        asp = app_service.id
        rg_name = resource_group.name
        python_version = self.python_version

        self._from_az = self.cli.invoke(
            f'webapp create -g {rg_name} -p {asp} -n {name} --runtime PYTHON:{python_version}',
            tags={**resource_group.tags, **app_service.tags}
        )
        self.cli.invoke(
            ' '.join((
                f'webapp config set --resource-group {rg_name} --name {name}',
                '--web-sockets-enabled true',
                '--http20-enabled',
                '--startup-file weblodge.startup',
                f'--always-on {app_service.always_on_supported}',
            ))
        )

    def delete(self):
        """
        Delete the WebApp.
        """
        self.cli.invoke(
            f'webapp delete -g {self.resource_group.name} -n {self.name}',
            to_json=False
        )

    def deploy(self, src: str) -> None:
        """
        Deploy an application zipped.
        """
        self.cli.invoke(
            ' '.join((
                'webapp deployment source config-zip',
                f'-g {self.resource_group.name} -n {self.name}',
                f'--src {src}'
            ))
        )

    def logs(self) -> None:
        """
        Stream WebApp logs.
        This is a blocking operation. User must run CTRL+C to stop the process.
        """
        self.cli.invoke(
            f'webapp log tail -g {self.resource_group.name} -n {self.name}'
        )
