# pylint: disable=consider-using-from-import

"""
Entry point for the CLI.

This module is the entry point for the CLI. It parses the command line arguments
and calls the appropriate functions.
"""
import logging
from typing import Dict

import weblodge.state as state
import weblodge.web_app as web_app
import weblodge.parameters as parameters
from weblodge.config import Item as ConfigItem


logger = logging.getLogger('weblodge')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


# pylint: disable=missing-function-docstring
def main():
    weblodge = parameters.weblodge()
    config_filename = weblodge.config_filename

    config = state.load(config_filename)

    if weblodge.action == 'build':
        config = build(config)
    elif weblodge.action == 'deploy':
        config = deploy(config)
    elif weblodge.action == 'delete':
        config = delete(config)

    state.dump(config_filename, config)


def build(config: Dict[str, str]) -> Dict[str, str]:
    """
    Build the application.
    """
    logger.info('Building...')
    config = parameters.load(
        web_app.build_config(),
        config
    )
    web_app.build(config)
    logger.info('Successfully built.')
    return config


def deploy(config: Dict[str, str]) -> Dict[str, str]:
    """
    Deploy the application.
    """
    # The application can be built before being deployed.
    deploy_can_build = [
        ConfigItem(
            name='build',
            description='Build then deploy the application.',
            attending_value=False
        )
    ]
    must_build = parameters.load(deploy_can_build, config)

    if must_build.pop('build'):
        config = build(config)

    logger.info('Deploying...')
    config = parameters.load(
        web_app.deploy_config(),
        config
    )
    webapp_url = web_app.deploy(config)
    logger.info(f"Successfully deployed at 'https://{webapp_url}'.")
    return config


def delete(config: Dict[str, str]) -> Dict[str, str]:
    """
    Delete the application.
    """
    do_not_prompt = parameters.load([
        ConfigItem(
            name='yes',
            description='Delete without user input.',
            attending_value=False
        )],
        config
    )

    if not do_not_prompt.get('yes'):
        if input('Are you sure you want to delete the application (yes/no.)? ') != 'yes':
            logger.info('Aborting.')
            return config

    logger.info('Deleting...')
    config = parameters.load(
        web_app.delete_config(),
        config
    )
    web_app.delete(config)
    logger.info('Successfully deleted.')

    return config
