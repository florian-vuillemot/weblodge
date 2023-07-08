"""
Azure Web App representation.
"""
from typing import List, Dict
from dataclasses import dataclass

from .cli import Cli
from .resource_group import ResourceGroupModel, ResourceGroup
from .appservice import AppServiceModel, AppService


@dataclass(frozen=True)
class WebAppModel:  # pylint: disable=too-many-instance-attributes
    """
    Azure WebApp representation.
    """
    name: str
    kind: str
    location: str
    host_names: List[str]
    linux_fx_version: str
    app_service: AppServiceModel
    resource_group: ResourceGroupModel
    tags: Dict[str, str]


class WebApp:
    """
    Helper class to manage Azure WebApps.
    """
    def __init__(self, cli: Cli()) -> None:
        self._cli = cli
        self._resources = []

    def list(self, force_reload=False) -> List[WebAppModel]:
        """
        List all WebApps.
        """
        if force_reload:
            self._resources.clear()

        if not self._resources:
            web_apps = self._cli.invoke('webapp list')
            resource_group_helper = ResourceGroup(self._cli)

            for web_app in web_apps:
                self._resources.append(
                    WebAppModel(
                        name=web_app['name'],
                        host_names=web_app['hostNames'],
                        kind=web_app['kind'],
                        location=web_app['location'],
                        linux_fx_version=web_app['siteConfig']['linuxFxVersion'],
                        app_service=AppService(self._cli).get(id_=web_app['appServicePlanId']),
                        resource_group=resource_group_helper.get(web_app['resourceGroup']),
                        tags=web_app['tags']
                    )
                )

        return self._resources

    def get(self, name: str, force_reload=False) -> WebAppModel:
        """
        Return a WebApp by its name.
        """
        for webapp in self.list(force_reload=force_reload):
            if webapp.name == name:
                return webapp

        raise Exception(f"WebApp '{name}' not found.")  # pylint: disable=broad-exception-raised

    def delete(self, webapp: WebAppModel) -> List[WebAppModel]:
        """
        Delete a WebApp.
        """
        self._cli.invoke(
            f'webapp delete -g {webapp.resource_group.name} -n {webapp.name}',
            to_json=False
        )
        return self.list(force_reload=True)

    # pylint: disable=too-many-arguments
    def create(
            self,
            name: str,
            app_service: AppServiceModel,
            resource_group: ResourceGroupModel = None,
            python_version: str = '3.10',
            tags: Dict[str, str] = None
        ) -> WebAppModel:
        """
        Create a new WebApp.

        Settings enabled:
        - WebSockets
        - HTTP/2
        - Always On
        """
        rg_name = resource_group.name if resource_group else app_service.resource_group.name

        self._cli.invoke(
            f'webapp create -g {rg_name} -p {app_service.id} -n {name} --runtime PYTHON:{python_version}',  # pylint: disable=line-too-long
            tags=tags
        )
        self._cli.invoke(
            ' '.join((
                f'webapp config set --resource-group {rg_name} --name {name}',
                '--web-sockets-enabled true',
                '--http20-enabled',
                '--always-on true'
            ))
        )
        return self.get(name, force_reload=True)

    def deploy(self, webapp: WebAppModel, src: str) -> None:
        """
        Deploy an application zipped to the WebApp.
        """
        self._cli.invoke(
            ' '.join((
                'webapp deployment source config-zip',
                f'-g {webapp.resource_group.name} -n {webapp.name}',
                f'--src {src}'
            ))
        )

    def logs(self, webapp: WebAppModel) -> None:
        """
        Stream WebApp logs.
        This is a blocking operation. User must run CTRL+C to stop the process.
        """
        self._cli.invoke(
            f'webapp log tail -g {webapp.resource_group.name} -n {webapp.name}'
        )
