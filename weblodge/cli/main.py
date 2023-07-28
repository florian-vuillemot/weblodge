# pylint: disable=consider-using-from-import

"""
Entry point for the CLI.

This module is the entry point for the CLI. It parses the command line arguments
and calls the appropriate functions.
"""
import sys
import logging

from typing import Dict

import weblodge.state as state
from weblodge.web_app import WebApp
from weblodge.parameters import Parser, ConfigIsNotDefined, ConfigIsDefined, ConfigTrigger

from .args import get_cli_args, CLI_NAME


logger = logging.getLogger('weblodge')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

# pylint: disable=missing-function-docstring
def main():
    success = False
    parameters = Parser()
    action, config_file = get_cli_args()
    web_app = WebApp(parameters.load)

    try:
        config = state.load(config_file)
        if action == 'build':
            success, config = web_app.build(config)
        elif action == 'deploy':
            success, config = deploy(config, web_app, parameters)
        elif action == 'delete':
            success, config = delete(config, web_app, parameters)
        elif action == 'clean':
            success, config = clean(config, web_app, parameters)
        elif action == 'logs':
            print('Logs will be stream, execute CTRL+C to stop the application.', flush=True)
            web_app.print_logs(config)
    except Exception as exception: # pylint: disable=broad-exception-caught
        print('Command failed with the following error:', exception, file=sys.stderr, flush=True)

    if success:
        state.dump(config_file, config)
        return web_app

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

    parameters.trigger_once(build_too)
    success, config = web_app.deploy(config)

    if success:
        print(f"The application will soon be available at: {web_app.url()}", flush=True)
    else:
        print(
            'The application may not be deployed, but the infrastructure may be' \
            f' partially created. You can delete it by running: {CLI_NAME} delete',
            sys=sys.stderr,
            flush=True
        )
    return success, config


def delete(config: Dict[str, str], web_app: WebApp, parameters: Parser):
    """
    Delete the application.
    """
    prompt = ConfigIsNotDefined(
        name='yes',
        description='Delete without user input.',
        trigger=_validation_before_deletion,
        attending_value=False
    )

    parameters.trigger_once(prompt)
    return web_app.delete(config)


def clean(config: Dict[str, str], web_app: WebApp, parameters: Parser):
    """
    Iterate over all resources and ask the user if he want to delete them.
    The parameter 'yes' is too risquy to be accepted and will be ignored.
    """
    prompt = ConfigTrigger(
        name='yes',
        description='The user input will always be asked',
        trigger=_validation_before_deletion,
        attending_value=False
    )

    for name in web_app.all():
        try:
            parameters.trigger_once(prompt)
            web_app.delete({'subdomain': name})
        except SystemExit:
            # User aborted the deletion.
            continue

    return True, config


def _validation_before_deletion(config):
    if input(f"Are you sure you want to delete the application '{config['subdomain']}' (yes/no.)? ") != 'yes':
        print('Aborting.')
        sys.exit(0)
    return config
