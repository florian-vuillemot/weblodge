from dataclasses import dataclass

from .cli import Cli


@dataclass
class Subscription:
    """
    Azure Subscription representation.
    """
    id: str
    name: str


class SubscriptionHelper:
    """
    Helper class to manage Azure subscriptions.
    """

    def __init__(self, cli: Cli) -> None:
        self._cli = cli
        self._subscriptions = []

    def list(self) -> list[Subscription]:
        if not self._subscriptions:
            subscription = self._cli.invoke('account list')
            self._subscriptions = [Subscription(id=s['id'], name=s['name']) for s in subscription]

        return self._subscriptions

    def get(self, name: str) -> Subscription:
        """
        Return a subscription by its name.
        """
        for s in self.list():
            if s.name == name:
                return s

        raise Exception(f"Subscription '{name}' not found.")
