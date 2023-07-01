import logging

import weblodge.config as config
from weblodge.web_app import WebApp

logger = logging.getLogger('weblodge')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


def main():
    webapp = WebApp()
    weblodge = config.weblodge()

    if weblodge.action == 'build':
        build(webapp)
    elif weblodge.action == 'deploy':
        deploy(webapp)


def build(webapp: WebApp):
    """
    Build the application.
    """
    logger.info('Building...')
    webapp.build(
        config.load(webapp.config()['build'])
    )
    logger.info('Successfully built.')


def deploy(webapp: WebApp):
    """
    Deploy the application.
    """
    # User can choose to build the application before deploying it.
    deploy_can_build = [
        config.Field(
            name='build',
            description='Build then deploy the application.',
            attending_value=False
        )
    ]
    must_build = config.load(deploy_can_build)

    if must_build.pop('build'):
        build(webapp)

    logger.info('Deploying...')
    webapp_url = webapp.deploy(config.load(webapp.config()['deploy']))

    logger.info(f"Successfully deployed at 'https://{webapp_url}'.")
