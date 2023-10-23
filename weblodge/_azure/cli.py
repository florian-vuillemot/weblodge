"""
Interface to the Azure CLI.
"""
import json
import logging
from io import StringIO
import time
from typing import Dict, List, Optional, Union

from azure.cli.core import get_default_cli  # type: ignore

from .exceptions import CLIException


logger = logging.getLogger('weblodge')


class Cli:
    """
    Azure CLI wrapper.
    """
    def __init__(self):
        self._first_invoke = True
        self.cli = get_default_cli()

    # pylint: disable=too-many-arguments
    def invoke(
            self,
            command: str,
            to_json=True,
            tags: Optional[Dict[str, str]] = None,
            log_outputs: bool = False,
            command_args: Optional[List[str]] = None
        ) -> Union[str, Dict, List]:
        """
        Execute an Azure CLI command and return its output.
        If `to_json` is True, the output is converted to a JSON object.
        If `log_outputs` is True, the output is not returned but logged instead.
        `command_args` contains the arguments to add to the command as is without split.
        """
        command_args = command_args or []

        if self._first_invoke:
            self._first_invoke = False

            try:
                return self._invoke(
                    command,
                    to_json=to_json,
                    tags=tags,
                    log_outputs=log_outputs,
                    command_args=command_args
                )
            except Exception as exception:  # pylint: disable=broad-exception-caught
                if 'az login' in str(exception):
                    logger.info('Authentication is needed...')
                    self._invoke('login', to_json=False, tags=None, log_outputs=log_outputs, command_args=[])
                    logger.info('Login successful, retry previous command...')

        return self._invoke(command, to_json=to_json, tags=tags, log_outputs=log_outputs, command_args=command_args)

    # pylint: disable=too-many-arguments
    def _invoke(
        self,
        command: str,
        to_json: bool,
        tags: Union[Dict[str, str], None],
        log_outputs: bool,
        command_args: List[str]
    ) -> Union[str, Dict]:
        # Convert the string command to a array of arguments.
        cmd = command.split()
        cmd.extend(command_args)
        # Redirect the output to a file if the log output is not asked.
        out_fd = None if log_outputs else StringIO()

        if tags:
            cmd.append('--tags')
            cmd.extend(f'{k}={v}' for k, v in tags.items())

        exception = None
        for i in range(1, 15):
            try:
                # Execute the Azure CLI command.
                if self.cli.invoke(cmd, out_file=out_fd):
                    exception = CLIException(f"Error during execution of the command '{command}'.")  # pylint: disable=broad-exception-raised
                else:
                    exception = None
                    break
            except (SystemExit, Exception) as _exception: # pylint: disable=broad-exception-caught
                exception = CLIException(f"Error during execution of the command '{command}'.\nTraceback: {_exception}") # pylint: disable=raise-missing-from
            time.sleep(i)

        if exception:
            raise exception

        # No output to return.
        if log_outputs:
            return None

        # Retrieve the output.
        output = out_fd.getvalue()
        out_fd.close()

        # Convert the output to a JSON object if needed.
        if to_json:
            return json.loads(output)

        return output
