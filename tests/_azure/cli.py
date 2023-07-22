"""
CLI Mock that will return waiting output or exception
when a command is invoked.
"""
from typing import Dict, Union


class Cli:
    """
    Azure CLI Mock wrapper.
    Return waiting output or exception for a given command.
    The output can be a list of output, the next one will be returned.
    """
    def __init__(self, output):
        self.output = output

    def invoke(self, command: str, *_args, **_kwargs) -> Union[str, Dict]:
        """
        Invoke the given command and return the expected output.
        """
        assert command is not None, 'No command set.'
        assert self.output, 'No expected output set.'

        if isinstance(self.output, list):
            expected_output = self.output.pop(0)
        else:
            expected_output = self.output
            # Can only be called once.
            self.output = None

        if isinstance(expected_output, Exception):
            raise expected_output
        return expected_output
