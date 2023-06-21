import json
from io import StringIO
from typing import Dict, Union

from azure.cli.core import get_default_cli


class Cli:
    """
    Azure CLI wrapper.
    """
    def __init__(self):
        self.cli = get_default_cli()

    def invoke(self, command: str, to_json=True) -> Union[str, Dict]:
        """
        Execute an Azure CLI command and return its output.
        If `to_json` is True, the output is converted to a JSON object.
        """

        # Convert the string command to a array of arguments.
        cmd = command.split()
        # Create a file-like object to store the output.
        out_fd = StringIO()

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
