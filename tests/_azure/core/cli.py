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
