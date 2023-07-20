"""
CLI Mock that will return waiting output or exception
when a command is invoked.
"""
from typing import Dict, Union


class Cli:
    """
    Azure CLI Mock wrapper.
    Return waiting output or exception for a given command.
    """
    def __init__(self, output):
        self.output = output

    def invoke(self, command: str, *_args, **_kwargs) -> Union[str, Dict]:
        """
        Invoke the given command and return the expected output.
        """
        assert command is not None, 'No command set.'
        assert self.output is not None, 'No expected output set.'

        expected_output = self.output
        # Can only be called once.
        self.output = None
        if isinstance(expected_output, Exception):
            raise expected_output
        return expected_output
