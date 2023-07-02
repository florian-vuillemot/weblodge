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
        config = build(config)
    elif weblodge.action == 'deploy':
        config = deploy(config)

    state.dump(weblodge.config_filename, config)


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
    print(config)
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
    print(config)
    logger.info(f"Successfully deployed at 'https://{webapp_url}'.")
    return config
