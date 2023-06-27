from dataclasses import dataclass
from typing import List

from .resource_group import ResourceGroupModel, ResourceGroup
from .appservice import AppServiceModel, AppService

from .resource import Resource


@dataclass
class WebAppModel:
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


class WebApp(Resource):
    """
    Helper class to manage Azure WebApps.
    """
    def list(self, force_reload=False) -> List[WebAppModel]:
        """
        List all WebApps.
        """
        if force_reload:
            self._resources.clear()

        if not self._resources:
            web_apps = self._cli.invoke('webapp list')
            resource_group_helper = ResourceGroup(self._cli)
            
            for w in web_apps:
                web_app = WebAppModel(
                    name=w['name'],
                    host_names=w['hostNames'],
                    kind=w['kind'],
                    location=w['location'],
                    linux_fx_version=w['siteConfig']['linuxFxVersion'],
                    app_service=AppService(self._cli).get(id_=w['appServicePlanId']),
                    resource_group=resource_group_helper.get(w['resourceGroup']),
                )
                self._resources.append(web_app)

        return self._resources

    def get(self, name: str, force_reload=False) -> WebAppModel:
        """
        Return a WebApp by its name.
        """
        for s in self.list(force_reload=force_reload):
            if s.name == name:
                return s

        raise Exception(f"WebApp '{name}' not found.")

    def delete(self, webapp: WebAppModel) -> List[WebAppModel]:
        """
        Delete a WebApp.
        """
        self._cli.invoke(f'webapp delete -g {webapp.resource_group.name} -n {webapp.name}', to_json=False)
        return self.list(force_reload=True)

    def create(self, name: str, app_service: AppServiceModel, resource_group: ResourceGroupModel = None, python_version: str = '3.10') -> WebAppModel:
        """
        Create a new WebApp.
        """
        rg_name = resource_group.name if resource_group else app_service.resource_group.name
        self._cli.invoke(
            f'webapp create -g {rg_name} -p {app_service.id} -n {name} --runtime PYTHON:{python_version}'
        )
        return self.get(name, force_reload=True)
    
    def deploy(self, webapp: WebAppModel, src: str) -> None:
        """
        Deploy an application zipped to the WebApp.
        """
        rg = webapp.resource_group.name
        wa = webapp.name

        self._cli.invoke(
            f'webapp deployment source config-zip -g {rg} -n {wa} --src {src}'
        )
