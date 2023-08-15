"""
CLI Mock that will return waiting output or exception
when a command is invoked.
"""
from typing import Dict, Iterable, Union


class Cli:
    """
    Azure CLI Mock wrapper.
    Return waiting output or exception for a given command.
    The output can be a list of output, the next one will be returned.
    """
    def __init__(self, output):
        self.output = output
        self.commands = []

    def invoke(self, command: str, *_args, **_kwargs) -> Union[str, Dict]:
        """
        Invoke the given command and return the expected output.
        """
        assert command is not None, 'No command set.'
        assert self.output, 'No expected output set.'

        self.commands.append(command)

        if isinstance(self.output, list):
            expected_output = self.output.pop(0)
        else:
            expected_output = self.output
            # Can only be called once.
            self.output = None

        if isinstance(expected_output, Exception):
            raise expected_output
        return expected_output

    def asserts_commands_called(self, commands: Iterable[str]):
        """
        Assert that the given commands were invoked.
        """
        for command in commands:
            for command_called in self.commands:
                if command in command_called:
                    break
            else:
                assert False, f'Command "{command}" not called.'

    def asserts_commands_not_called(self, commands: Iterable[str]):
        """
        Assert that the given commands were not invoked.
        """
        for command in commands:
            for command_called in self.commands:
                assert command not in command_called, f'Command "{command}" not called.'
