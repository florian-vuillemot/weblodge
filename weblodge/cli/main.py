import logging
from typing import Dict

import weblodge.parameters as parameters
import weblodge.state as state
import weblodge.web_app as web_app
from weblodge.config import Item as ConfigItem


logger = logging.getLogger('weblodge')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


def main():
    weblodge = parameters.weblodge()

    config = state.load(weblodge.config_filename)

    if weblodge.action == 'build':
        build(config)
    elif weblodge.action == 'deploy':
        deploy(config)


def build(config: Dict[str, str]):
    """
    Build the application.
    """
    logger.info('Building...')
    params = parameters.load(
        web_app.Build.config,
        config
    )
    web_app.Build(**params).build()
    logger.info('Successfully built.')


def deploy(config: Dict[str, str]):
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
        build(config)

    logger.info('Deploying...')
    params = parameters.load(
        web_app.Deploy.config,
        config
    )
    webapp_url = web_app.Deploy(**params).deploy()

    logger.info(f"Successfully deployed at 'https://{webapp_url}'.")
