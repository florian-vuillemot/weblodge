from dataclasses import dataclass
from typing import List

from .cli import Cli


@dataclass
class WebApp:
    """
    Azure WebApp representation.
    """
    name: str
    resource_group: str
    host_names: List[str]
    kind: str
    location: str
    linux_fx_version: str


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
            for w in web_apps:
                web_app = WebApp(
                    name=w['name'],
                    resource_group=w['resourceGroup'],
                    host_names=w['hostNames'],
                    kind=w['kind'],
                    location=w['location'],
                    linux_fx_version=w['siteConfig']['linuxFxVersion']
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
