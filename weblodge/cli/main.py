# pylint: disable=consider-using-from-import

"""
Entry point for the CLI.

This module is the entry point for the CLI. It parses the command line arguments
and calls the appropriate functions.
"""
import sys
import logging
import argparse

from typing import Dict

import weblodge.state as state

from weblodge.parameters import Parser, ConfigIsNotDefined, ConfigIsDefined
from weblodge.web_app import WebApp


logger = logging.getLogger('weblodge')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

# Command Line Interface name.
CLI_NAME = sys.argv[0]


def get_weblodge_parameters():
    """
    Return default parameters.
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
        choices=['build', 'deploy', 'delete', 'logs']
    )
    _parser.add_argument(
        '--config-filename',
        type=str,
        help='File containing the deployment configuration.',
        default='.weblodge.json',
        required=False
    )
    args, _ = _parser.parse_known_args()

    return args.action, args.config_filename


# pylint: disable=missing-function-docstring
def main():
    parameters = Parser()
    action, config_filename = get_weblodge_parameters()
    web_app = WebApp(parameters.load)

    config = state.load(config_filename)
    if action == 'build':
        success, config = web_app.build(config)
    elif action == 'deploy':
        success, config = deploy(config, web_app, parameters)
    elif action == 'delete':
        success, config = delete(config, web_app, parameters)
    elif action == 'logs':
        logger.warning('Logs will be stream, execute CTRL+C to stop the application.')
        web_app.print_logs(config)

    if success:
        state.dump(config_filename, config)
        return config

    sys.exit(1)


def deploy(config: Dict[str, str], web_app: WebApp, parameters: Parser):
    """
    Deploy the application.
    """
    # The application can be built before being deployed.
    def _build(config):
        success, config = web_app.build(config)

        if not success:
            logger.critical('Deployment failed.')
            sys.exit(1)
        return config

    build_too = ConfigIsDefined(
        name='build',
        description='Build then deploy the application. Parameters are the same as for the `build` command.',
        attending_value=False,
        trigger=_build
    )

    with parameters.add_trigger(build_too):
        success, config = web_app.deploy(config)

    if success:
        logger.info(f"The application will soon be available on: https://{web_app.url()}")
    else:
        logger.critical(
            'The application may not be deployed, but the infrastructure may be' \
            f' partially created. You can delete it by running: {CLI_NAME} delete'
        )
    return success, config


def delete(config: Dict[str, str], web_app: WebApp, parameters: Parser):
    """
    Delete the application.
    """
    def _validation(config):
        if input('Are you sure you want to delete the application (yes/no.)? ') != 'yes':
            logger.info('Aborting.')
            sys.exit(0)
        return config

    prompt = ConfigIsNotDefined(
        name='yes',
        description='Delete without user input.',
        trigger=_validation,
        attending_value=False
    )

    with parameters.add_trigger(prompt):
        return web_app.delete(config)
