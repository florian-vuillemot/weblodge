"""
Command Line Interface arguments.
"""
import sys
import argparse
from typing import Tuple

# Default configuration filename.
DEFAULT_CONFIG_FILE = '.weblodge.json'

# Command Line Interface name.
CLI_NAME = sys.argv[0]


def get_cli_args() -> Tuple[str, str]:
    """
    Return the action to perform and the configuration filename.
    """
    # If run user run: `python weblodge.py -h` or `python weblodge.py --help`
    # then we want to display the **WebLodge** `help` message.
    # Otherwise, we want to parse the arguments and better scope the help message.
    # Example: `python weblodge.py build -h` must print the `help` message for the `build` action.
    asking_global_help = len(sys.argv) == 2 and '-h' in sys.argv[1]

    _parser = argparse.ArgumentParser(
        description='Deploy a Python Flask-based application to Azure.',
        add_help=asking_global_help
    )
    _parser.add_argument(
        'action',
        type=str,
        help='Action to perform.',
        choices=['build', 'clean', 'deploy', 'delete', 'github', 'list', 'logs', 'app-tiers']
    )
    _parser.add_argument(
        '--config-file',
        type=str,
        help='File containing the deployment configuration.',
        default=DEFAULT_CONFIG_FILE,
        required=False
    )
    args, _ = _parser.parse_known_args()

    return args.action, args.config_file
