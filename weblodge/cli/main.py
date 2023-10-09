# pylint: disable=consider-using-from-import

"""
Entry point for the CLI.

This module is the entry point for the CLI. It parses the command line arguments
and calls the appropriate functions.
"""
import sys
import logging
from typing import Dict
from pathlib import Path
from collections import defaultdict


import weblodge.state as state
from weblodge._azure import Service
from weblodge.parameters import Parser, ConfigIsNotDefined, ConfigIsDefined, ConfigTrigger
from weblodge.web_app import WebApp, NoMoreFreeApplicationAvailable, CanNotFindTierLocation, InvalidTier

from .args import get_cli_args, CLI_NAME


# Define the logger for internal usage.
# But the CLI will use print for user interraction.
logger = logging.getLogger('weblodge')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


# pylint: disable=missing-function-docstring
def main(return_web_app=False):
    success = False
    parameters = Parser()
    action, config_file = get_cli_args()
    web_app = WebApp(parameters.load, azure_service=Service())

    try:
        config = state.load(config_file)
        if action == 'build':
            success, config = web_app.build(config)
        elif action == 'clean':
            success = clean(parameters, web_app)
        elif action == 'deploy':
            success, config = deploy(config, web_app, parameters)
        elif action == 'delete':
            success = delete(config, web_app, parameters)
        elif action == 'github':
            success, config = github(config, web_app, config_file)
        elif action == 'list':
            list_(parameters.load, web_app)
            success = True
        elif action == 'logs':
            print('Logs will be stream, execute CTRL+C to stop the application.', flush=True)
            web_app.print_logs(config)
        elif action == 'app-tiers':
            success = list_app_tiers(config, web_app)
    except Exception as exception: # pylint: disable=broad-exception-caught
        print('Command failed with the following error:', exception, file=sys.stderr, flush=True)

    if success:
        state.dump(config_file, config)
        if return_web_app:
            return web_app
        return 0

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
        success, config, tier = web_app.deploy(config)
    except NoMoreFreeApplicationAvailable as free_app_name:
        print(
            'Can not create the infrastrucutre. Azure support only one Free application by location.',
            'Please, change the deployment location or the application tier.',
            f"The already existing free application is this location is '{free_app_name}'.",
            file=sys.stderr,
            flush=True
        )
        return False, config
    except InvalidTier as _invalid_tier:
        print(
            'Invalid tier. Please, choose a tier from the following list:',
            file=sys.stderr,
            flush=True
        )
        list_app_tiers(config, web_app)
        return False, config

    print(f'Estimated cost: ${tier.price_by_hour * 730:.2f}/month')

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


def clean(parameters: Parser, web_app: WebApp):
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

    for _wa in web_app.all(parameters.load):
        try:
            parameters.trigger_once(prompt)
            _wa.delete()
        except SystemExit:
            # User aborted the deletion.
            continue

    return True


def github(config: Dict[str, str], web_app: WebApp, config_file: str):
    """
    Create a GitHub application.
    """
    workflow_folder: str = '.github/workflows'
    workflow_file: str = '.github/workflows/weblodge.yml'

    config, workflow = web_app.github(config)

    if workflow:
        # Create the GitHub workflow folder if not exists.
        Path(workflow_folder).mkdir(parents=True, exist_ok=True)
        # Create the GitHub workflow file.
        Path(workflow_file).write_text(workflow.content, encoding='utf-8')

        # pylint: disable=line-too-long
        print(f'''Please, add the following secrets to your GitHub repository:
  - AZURE_CLIENT_ID: {workflow.client_id}
  - AZURE_TENANT_ID: {workflow.tenant_id}
  - AZURE_SUBSCRIPTION_ID: {workflow.subscription_id}
Then, commit and push the following files:
  - {workflow_file}
  - {config_file}
More information: https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository''')

    return True, config


def list_app_tiers(config, web_app) -> bool:
    """
    Show to the user the available tiers.
    """
    try:
        # Retrieve the tiers.
        tiers = web_app.tiers(config)
    except CanNotFindTierLocation:
        print('Can not find any tier for the provided location.', file=sys.stderr, flush=True)
        print('Please, check the location and try again.', file=sys.stderr, flush=True)
        return False

    print('Warning: There is no guarantee of the estimated price.')

    # Group the tiers by description to print them by blocks.
    tiers_by_description = defaultdict(list)
    for tier in tiers:
        tiers_by_description[tier.description].append(tier)
        # Sort by cores to have a nice display.
        tiers_by_description[tier.description].sort(key=lambda t: t.cores)

    # Print the tiers.
    for description, tiers in tiers_by_description.items():
        # If the list is not empty, print the information.
        if tiers:
            print(f'\nTier description: {description}')
            print(f'Tier location: {tiers[0].location}')
            print(' Name |    Price    | Cores |   RAM   | Storage')
            print('-----------------------------------------------')
            for tier in tiers:
                print(f'{tier.name:>5} |  ${tier.price_by_hour:.2f}/hour |    {tier.cores:>2} | {tier.ram:>4} GB |  {str(tier.disk) + " GB":>6}')  # pylint: disable=line-too-long

    return True

def list_(parameter_loader, web_app: WebApp):
    """
    Print all the deployed applications.
    Warm the user if some infrastructure is not used.
    """
    unused_apps = []
    no_application_deployed = True

    for _wapp in web_app.all(parameter_loader):
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
    if input(f"Do you want to delete the application '{config['subdomain']}' (yes/no.)? ") != 'yes':
        print('Aborting.')
        sys.exit(0)
    return config
