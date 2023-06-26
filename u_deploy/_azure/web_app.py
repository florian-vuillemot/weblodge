from dataclasses import dataclass
from typing import List

from .resource_group import ResourceGroup, ResourceGroupHelper
from .appservice import AppService, AppServiceHelper

from .cli import Cli


@dataclass
class WebApp:
    """
    Azure WebApp representation.
    """
    name: str
    kind: str
    location: str
    host_names: List[str]
    linux_fx_version: str
    app_service: AppService
    resource_group: ResourceGroup


class WebAppHelper:
    """
    Helper class to manage Azure WebApps.
    """

    def __init__(self, cli: Cli) -> None:
        self._cli = cli
        self._web_apps = []

    def list(self, force_reload=False) -> list[WebApp]:
        """
        List all WebApps.
        """
        if force_reload:
            self._web_apps.clear()

        if not self._web_apps:
            web_apps = self._cli.invoke('webapp list')
            resource_group_helper = ResourceGroupHelper(self._cli)
            
            for w in web_apps:
                web_app = WebApp(
                    name=w['name'],
                    host_names=w['hostNames'],
                    kind=w['kind'],
                    location=w['location'],
                    linux_fx_version=w['siteConfig']['linuxFxVersion'],
                    app_service=AppServiceHelper(self._cli).get(id_=w['appServicePlanId']),
                    resource_group=resource_group_helper.get(w['resourceGroup']),
                )
                self._web_apps.append(web_app)

        return self._web_apps

    def get(self, name: str, force_reload=False) -> WebApp:
        """
        Return a WebApp by its name.
        """
        for s in self.list(force_reload=force_reload):
            if s.name == name:
                return s

        raise Exception(f"WebApp '{name}' not found.")

    def delete(self, webapp: WebApp) -> List[WebApp]:
        """
        Delete a WebApp.
        """
        self._cli.invoke(f'webapp delete -g {webapp.resource_group.name} -n {webapp.name}', to_json=False)
        return self.list(force_reload=True)

    def create(self, name: str, app_service: AppService, resource_group: ResourceGroup = None, python_version: str = '3.10') -> WebApp:
        """
        Create a new WebApp.
        """
        rg_name = resource_group.name if resource_group else app_service.resource_group.name
        self._cli.invoke(
            f'webapp create -g {rg_name} -p {app_service.id} -n {name} --runtime PYTHON:{python_version}'
        )
        return self.get(name, force_reload=True)
    
    def deploy(self, webapp: WebApp, src: str) -> None:
        """
        Deploy an application zipped to the WebApp.
        """
        rg = webapp.resource_group.name
        wa = webapp.name

        self._cli.invoke(
            f'webapp deployment source config-zip -g {rg} -n {wa} --src {src}'
        )
