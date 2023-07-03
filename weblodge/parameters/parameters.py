import argparse
from dataclasses import dataclass
from typing import Any, Dict, List

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
    parser = argparse.ArgumentParser(description='Deploy a Python Flask-based application to Azure.')
    parser.add_argument('action', type=str, help='Action to perform.', choices=['build', 'deploy'])
    parser.add_argument('--config-filename', type=str, help='File containing the deployment configuration.', default=Global.config_filename, required=False)
    args, _ = parser.parse_known_args()

    return Global(
        action=args.action,
        config_filename=args.config_filename
    )


def load(fields: List[ConfigItem], current_config: Dict[str, str] = {}) -> Dict[str, str]:
    """
    Load the configuration from the parser.
    Override the current config with the new values.
    """
    # Create and configure a parser for the fields.
    parser = argparse.ArgumentParser()
    for field in fields:
        argument = {
            'help': field.description,
        }

        if not field.attending_value:
            argument['action'] = 'store_true'
        else:
            argument = {
                **argument,
                'type': str,
                'required': field.default is None
            }

        parser.add_argument(
            f'--{_to_display(field.name)}',
            **argument
        )
    args_parsed, _ = parser.parse_known_args()
    
    # If the user did not specify a value, use the value passed in parameter 
    # otherwise the default one.
    new_config = {}
    for field in fields:
        value_if_not_defined = current_config.get(field.name, field.default)
        new_config[field.name] = getattr(args_parsed, field.name) or value_if_not_defined

    return {**current_config, **new_config}


def _to_display(name: str) -> str:
    return name.replace('_', '-')
