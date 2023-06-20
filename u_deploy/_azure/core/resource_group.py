from dataclasses import dataclass

from .cli import Cli


@dataclass
class ResourceGroup:
    name: str
    location: str


class ResourceGroupHelper:
    def __init__(self, cli: Cli) -> None:
        self._cli = cli
        self.resource_groups = []

    def list(self) -> list[ResourceGroup]:
        """
        List all Resource Group.
        """
        if not self.resource_groups:
            rgs = self._cli.invoke('group list')
            for s in rgs:
                a = ResourceGroup(
                        name=s['name'],
                        location=s['location']
                )
                self.resource_groups.append(a)

        return self.resource_groups
    
    def get(self, name: str) -> ResourceGroup:
        """
        Return an resource group by its name.
        """
        for s in self.list():
            if s.name == name:
                return s

        raise Exception(f"Resource Group '{name}' not found.")
