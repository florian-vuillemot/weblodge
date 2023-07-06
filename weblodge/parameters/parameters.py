"""
User inputs can be provided by command line.
This package contains the logic to parse the command line arguments for internal
components based on the configuration items. but also the global arguments that are
hard coded.
"""
import argparse
from dataclasses import dataclass
from typing import Dict, List

from weblodge.config import Item as ConfigItem


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
    parser = argparse.ArgumentParser(
        description='Deploy a Python Flask-based application to Azure.'
    )
    parser.add_argument(
        'action',
        type=str,
        help='Action to perform.',
        choices=['build', 'deploy', 'delete']
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
