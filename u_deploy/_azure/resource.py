from .cli import Cli


class Resource:
    def __init__(self, cli: Cli) -> None:
        self._cli = Cli()
        self._resources = []
