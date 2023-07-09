"""
User inputs can be provided by command line.
This package contains the logic to parse the command line arguments for internal
components based on the configuration items. but also the global arguments that are
hard coded.

The help method must be adapted to the action to be carried out.
Examples:
    `python weblodge.py -h` must print the `help` message of **WebLodge**.
    `python weblodge.py build -h` must print the `help` message for the `build` action.
"""
import sys
import argparse
from dataclasses import dataclass
from typing import Dict, List

from weblodge.config import Item as ConfigItem


# Command Line Interface name.
CLI_NAME = sys.argv[0]


@dataclass(frozen=True)
class Global:
    """
    Global and pre defined configuration.
    """
    # The action to perform.
    action: str
    # The configuration file name containing the deployment state.
    config_filename: str = '.weblodge.json'


def weblodge() -> str:
    """
    Return the action to perform.
    """
    # If run user run: `python weblodge.py -h` or `python weblodge.py --help`
    # then we want to display the **WebLodge** `help` message.
    # Otherwise, we want to parse the arguments and better scope the help message.
    # Example: `python weblodge.py build -h` must print the `help` message for the `build` action.
    asking_global_help = len(sys.argv) == 2 and '-h' in sys.argv[1]

    parser = argparse.ArgumentParser(
        description='Deploy a Python Flask-based application to Azure.',
        add_help=asking_global_help
    )
    parser.add_argument(
        'action',
        type=str,
        help='Action to perform.',
        choices=['build', 'deploy', 'delete', 'logs']
    )
    parser.add_argument(
        '--config-filename',
        type=str,
        help='File containing the deployment configuration.',
        default=Global.config_filename,
        required=False
    )
    args, _ = parser.parse_known_args()

    return Global(
        action=args.action,
        config_filename=args.config_filename
    )


def load(fields: List[ConfigItem], existing_parameters: Dict[str, str] = None) -> Dict[str, str]:
    """
    Load the configuration from the parser.
    Override the current config with the new values.
    """
    existing_parameters = existing_parameters or {}

    # Create and configure a parser for the fields.
    parser = argparse.ArgumentParser()
    for field in fields:
        argument = {
            'help': field.description,
        }

        default_value = existing_parameters.get(field.name, field.default)

        if not field.attending_value:
            argument['action'] = 'store_true'
        else:
            argument = {
                **argument,
                'type': str,
                'required': default_value is None,
                'default': default_value,
            }

        parser.add_argument(
            f'--{_to_display(field.name)}',
            **argument
        )
    args_parsed, _ = parser.parse_known_args()

    return {**existing_parameters, **vars(args_parsed)}


def _to_display(name: str) -> str:
    return name.replace('_', '-')
