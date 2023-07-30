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
from weblodge.web_app import WebApp, FreeApplicationAlreadyDeployed
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
        elif action == 'clean':
            success = clean(parameters)
        elif action == 'deploy':
            success, config = deploy(config, web_app, parameters)
        elif action == 'delete':
            success = delete(config, web_app, parameters)
        elif action == 'list':
            list_(parameters.load)
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
    try:
        success, config = web_app.deploy(config)
    except FreeApplicationAlreadyDeployed as free_app_name:
        print(
            'Can not create the infrastrucutre. Azure support only one Free application by location.',
            'Please, change the deployment location or the application sku.',
            f"The already existing free application is this location is '{free_app_name}'.",
            file=sys.stderr,
            flush=True
        )
        return False, config

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
    res, _ = web_app.delete(config)
    return res


def clean(parameters: Parser):
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

    for web_app in WebApp.all(parameters.load):
        try:
            parameters.trigger_once(prompt)
            web_app.delete()
        except SystemExit:
            # User aborted the deletion.
            continue

    return True


def list_(parameter_loader):
    """
    Print all the deployed applications.
    Warm the user if some infrastructure is not used.
    """
    unused_apps = []
    no_application_deployed = True

    for _wapp in WebApp.all(parameter_loader):
        no_application_deployed = False
        if _wapp.exists():
            print(f"Application: {_wapp.url()}")
        else:
            unused_apps.append(_wapp.name)

    if no_application_deployed:
        print('No application deployed.')
        return

    if unused_apps:
        print('We found the following infrastructure without application deployed. This can be costly.')
        for name in unused_apps:
            print(f"Application '{name}', can be deleted by running: `{CLI_NAME} delete --subdomain {name}`")


def _validation_before_deletion(config):
    if input(f"Are you sure you want to delete the application '{config['subdomain']}' (yes/no.)? ") != 'yes':
        print('Aborting.')
        sys.exit(0)
    return config
