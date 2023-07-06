"""
Azure Subscription representation.
"""
from typing import List
from dataclasses import dataclass

from .cli import Cli


@dataclass(frozen=True)
class SubscriptionModel:
    """
    Azure Subscription representation.
    """
    id: str  # pylint: disable=invalid-name
    name: str


class Subscription:
    """
    Helper class to manage Azure subscriptions.
    """
    def __init__(self, cli: Cli()) -> None:
        self._cli = cli
        self._resources = []

    def list(self) -> List[SubscriptionModel]:
        """
        Return the list of subscriptions.
        """
        if not self._resources:
            subscription = self._cli.invoke('account list')
            self._resources = [SubscriptionModel(id=s['id'], name=s['name']) for s in subscription]

        return self._resources

    def get(self, name: str) -> SubscriptionModel:
        """
        Return a subscription by its name.
        """
        for sub in self.list():
            if sub.name == name:
                return sub

        raise Exception(f"Subscription '{name}' not found.")  # pylint: disable=broad-exception-raised
