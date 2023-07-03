import json
from io import StringIO
import logging
from typing import Dict, Union

from azure.cli.core import get_default_cli


logger = logging.getLogger('weblodge')


class Cli:
    """
    Azure CLI wrapper.
    """
    def __init__(self):
        self._first_invoke = True
        self.cli = get_default_cli()

    def invoke(self, command: str, to_json=True, tags={}) -> Union[str, Dict]:
        """
        Execute an Azure CLI command and return its output.
        If `to_json` is True, the output is converted to a JSON object.
        """

        if self._first_invoke:
            self._first_invoke = False

            try:
                return self._invoke(command, to_json=to_json, tags=tags)
            except Exception as e:
                # Command may fail if the user is not logged in.
                logger.info(f"Previous command failed, try login to Azure CLI...")
                self._invoke('login')
                logger.info(f"Login successful, retry previous command...")

        return self._invoke(command, to_json=to_json, tags=tags)

    def _invoke(self, command: str, to_json=True, tags={}) -> Union[str, Dict]:
        # Convert the string command to a array of arguments.
        cmd = command.split()
        # Create a file-like object to store the output.
        out_fd = StringIO()

        if tags:
            cmd.append('--tags')
            for k, v in tags.items():
                cmd.append(f'{k}={v}')

        # Execute the Azure CLI command and store the return code.
        r = self.cli.invoke(cmd, out_file=out_fd)

        if r != 0:
            raise Exception(f"Error during execution of the command '{command}'.\nOutput: {r}")

        # Retrieve the output.
        output = out_fd.getvalue()
        out_fd.close()

        # Convert the output to a JSON object if needed.
        if to_json:
            return json.loads(output)

        return output
