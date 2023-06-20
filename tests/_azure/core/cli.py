import json
from pathlib import Path
from typing import Dict, Union


class Cli:
    """
    Azure CLI Mock wrapper.
    Return waiting output or exception for a given command.
    """
    def __init__(self):
        self._commands = {}

    def add_command(self, command: str, output = Union[Dict, str], to_json=True):
        """
        Add new command to the mock that will return the given output.
        """
        self._commands[(command, to_json)] = output

    def add_exception(self, command: str, to_json=True):
        """
        Raised an exception when the given command is invoked.
        """
        self._commands[(command, to_json)] = Exception

    def invoke(self, command: str, to_json=True) -> Union[str, Dict]:
        r = self._commands[(command, to_json)]
        if isinstance(r, Exception):
            raise r
        return r

# Create a default instance of the CLI that return working output.
cli = Cli()

resource_groups_json = json.loads(Path('./tests/_azure/core/mocks/resource_groups.json').read_text())
cli.add_command('group list', resource_groups_json)

appservices_json = json.loads(Path('./tests/_azure/core/mocks/appservices_plan.json').read_text())
cli.add_command('appservice plan list', appservices_json)

subscriptions_json = json.loads(Path('./tests/_azure/core/mocks/subscriptions.json').read_text())
cli.add_command('account list', subscriptions_json)

web_apps_json = json.loads(Path('./tests/_azure/core/mocks/web_apps.json').read_text())
cli.add_command('webapp list', web_apps_json)
