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
    elif weblodge.action == 'logs':
        logs(config)

    state.dump(config_filename, config)


def build(config: Dict[str, str]) -> Dict[str, str]:
    """
    Build the application.
    """
    config = parameters.load(
        web_app.build_config(),
        config
    )
    logger.info('Building...')
    web_app.build(config)
    logger.info('Successfully built.')
    return config


def deploy(config: Dict[str, str]) -> Dict[str, str]:
    """
    Deploy the application.
    """
    # The application can be built before being deployed.
    build_too = [
        ConfigItem(
            name='build',
            description='Build then deploy the application. Parameters are the same as for the `build` command.',
            attending_value=False
        )
    ]

    config = parameters.load(
        web_app.deploy_config() + build_too,
        config
    )

    if config['build']:
        build(config)

    logger.info('Deploying...')
    if webapp_url := web_app.deploy(config):
        logger.info(f"The application will soon be available on: https://{webapp_url}")
    else:
        logger.critical(
            'The application may not be deployed, but the infrastructure may be' \
            f' partially created. You can delete it by running: {parameters.CLI_NAME} delete'
        )
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

    config = parameters.load(
        web_app.delete_config(),
        config
    )
    logger.info('Deleting...')
    web_app.delete(config)
    logger.info('Successfully deleted.')

    return config


def logs(config: Dict[str, str]) -> None:
    """
    Stream application logs.
    """
    config = parameters.load(
        web_app.logs_config(),
        config
    )
    logger.warning('Logs will be stream, execute CTRL+C to stop the application.')
    logger.info('Recovering logs...')
    web_app.logs(config)
