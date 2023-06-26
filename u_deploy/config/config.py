import argparse
from dataclasses import dataclass
from typing import Any, List


@dataclass
class ConfigField:
    # Name of the field.
    # This name will be used as the command line argument, in the code and config files. 
    name: str
    # Description of the field. What is it used for?
    description: str
    # Example of the field, can be the default value.
    example: str
    # Default value of the field.
    # When specified, the field is optional.
    default: str = None


class Config:
    def __init__(self) -> None:
        self._parser = argparse.ArgumentParser(description='Deploy a Python Flask-based application to Azure.')
        self._parser.add_argument('target', type=str)
        self._parser.add_argument('action', type=str)

        self.args, _ = self._parser.parse_known_args()
        self.target = self.args.target
        self.action = self.args.action

    def load(self, fields: List[ConfigField]) -> None:
        """
        Load the configuration in the parser.
        """
        for field in fields:
            self._parser.add_argument(
                f'--{field.name}',
                type=str,
                help=field.description,
                default=field.default,
                required=field.default is None
            )
        self.args, _ = self._parser.parse_known_args()

    def __getitem__(self, name: str) -> Any:
        return getattr(self.args, name)
