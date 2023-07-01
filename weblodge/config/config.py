import argparse
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
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
    # List of choices for the field.
    choices: List[str] = None


def action() -> Dict[str, str]:
    """
    Return the action to perform.
    """
    parser = argparse.ArgumentParser(description='Deploy a Python Flask-based application to Azure.')
    parser.add_argument('action', type=str, help='Action to perform.', choices=['build', 'deploy'])
    args, _ = parser.parse_known_args()
    return args.action


def load(fields: List[Field]) -> Dict[str, str]:
    """
    Load the configuration in the parser.
    """
    res = {}

    # Create and configure a parser for the fields.
    parser = argparse.ArgumentParser()
    for field in fields:
        res[_to_arg_parse(field.name)] = field.default

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
            if field.choices:
                argument['choices'] = field.choices

        parser.add_argument(
            f'--{field.name}',
            **argument
        )
    args_parsed, _ = parser.parse_known_args()
    
    # Update the default values with the user values.
    for field in fields:
        n = _to_arg_parse(field.name)
        res[n] = getattr(args_parsed, n, res[n])

    return res


def _to_arg_parse(name: str) -> str:
    return name.replace('-', '_')