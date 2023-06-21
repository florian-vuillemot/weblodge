from dataclasses import dataclass
from typing import List

from u_deploy._azure import ResourceGroup, ResourceGroupHelper
from u_deploy._azure.core.appservice import AppService, AppServiceHelper

from .cli import Cli


@dataclass
class WebApp:
    """
    Azure WebApp representation.
    """
    name: str
    host_names: List[str]
    kind: str
    location: str
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

    def list(self) -> list[WebApp]:
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
                    app_service=AppServiceHelper(self._cli).get(
                        name=w['appServicePlanId'].split('/')[-1],
                        resource_group=resource_group_helper.get(w['appServicePlanId'].split('resourceGroups/')[1].split('/')[0])
                    ),
                    resource_group=resource_group_helper.get(w['resourceGroup']),
                )
                self._web_apps.append(web_app)

        return self._web_apps

    def get(self, name: str) -> WebApp:
        """
        Return a WebApp by its name.
        """
        for s in self.list():
            if s.name == name:
                return s

        raise Exception(f"WebApp '{name}' not found.")
