import argparse
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class Field:
    # Name of the field.
    # This name will be used as the command line argument, in the code and config files. 
    name: str
    # Description of the field. What is it used for?
    description: str
    # Does not expect a value from the user. The argument is a flag.
    # Example: --verbose
    attending_value: str = True
    # Default value of the field.
    # When specified, the field is optional.
    default: str = None


@dataclass(frozen=True)
class GlobalConfig:
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
    parser.add_argument('--config-filename', type=str, help='File containing the deployment configuration.', default=GlobalConfig.config_filename, required=False)
    args, _ = parser.parse_known_args()

    return GlobalConfig(
        action=args.action,
        config_filename=args.config_filename
    )


def load(fields: List[Field], current_config: Dict[str, str] = {}) -> Dict[str, str]:
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
                'default': field.default,
                'required': field.default is None
            }

        parser.add_argument(
            f'--{field.name}',
            **argument
        )
    args_parsed, _ = parser.parse_known_args()
    
    # If the user did not specify a value, use the value passed in parameter 
    # otherwise the default one.
    new_config = {}
    for field in fields:
        n = _to_arg_parse(field.name)
        value_if_not_defined = current_config.get(n, field.default)
        new_config[n] = getattr(args_parsed, n, value_if_not_defined)

    return {**current_config, **new_config}


def _to_arg_parse(name: str) -> str:
    return name.replace('-', '_')