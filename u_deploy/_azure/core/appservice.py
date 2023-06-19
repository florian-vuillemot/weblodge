from dataclasses import dataclass

from .cli import Cli


@dataclass
class AppService:
    name: str
    number_of_sites: int
    sku: str
    resource_group: str
    location: str


class AppServiceHelper:
    def __init__(self, cli: Cli) -> None:
        self._cli = cli
        self.appservices = []

    def list(self) -> list[AppService]:
        """
        List all AppServices Plan.
        """
        if not self.appservices:
            appservices = self._cli.invoke('appservice plan list')
            for s in appservices:
                a = AppService(
                        name=s['name'],
                        number_of_sites=int(s['numberOfSites']),
                        sku=s['sku']['name'],
                        resource_group=s['resourceGroup'],
                        location=s['location']
                )
                self.appservices.append(a)

        return self.appservices
    
    def get(self, name: str, resource_group: str = None) -> AppService:
        """
        Return an appservice by its name.
        """
        for s in self.list():
            if s.name == name:
                if resource_group is None or s.resource_group == resource_group:
                    return s

        raise Exception(f"AppService '{name}' not found.")
