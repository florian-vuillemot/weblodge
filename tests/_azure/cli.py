"""
CLI Mock that will return waiting output or exception for a given command using
pre defined Mocked output.
"""
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

    def invoke(self, command: str, to_json=True, tags=None) -> Union[str, Dict]:
        """
        Invoke the given command and return pre defined output.
        """
        output = self._commands[(command, to_json)]
        if isinstance(output, Exception):
            raise output
        return output

# Create a default instance of the CLI that return working output.
cli = Cli()

resource_groups_json = json.loads(
    Path('./tests/_azure/mocks/resource_groups.json').read_text()
)
cli.add_command('group list', resource_groups_json)
cli.add_command('group create --name staging --location northeurope', resource_groups_json[1])

appservices_json = json.loads(
    Path('./tests/_azure/mocks/appservices_plan.json').read_text(encoding='utf-8')
)
cli.add_command('appservice plan list', appservices_json)

subscriptions_json = json.loads(
    Path('./tests/_azure/mocks/subscriptions.json').read_text(encoding='utf-8')
)
cli.add_command('account list', subscriptions_json)

web_apps_json = json.loads(
    Path('./tests/_azure/mocks/web_apps.json').read_text(encoding='utf-8')
)
cli.add_command('webapp list', web_apps_json)
