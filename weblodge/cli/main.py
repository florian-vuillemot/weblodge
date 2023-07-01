import logging

import weblodge.config as config
from weblodge.web_app import WebApp


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def main():
    webapp = WebApp()
    action = config.action()

    if action == 'build':
        logging.info('Building...')
        webapp.build(
            config.load(webapp.config()['build'])
        )
        logging.info('Successfully built.')
    elif action == 'deploy':
        logging.info('Deploying...')
        webapp_url = deploy(webapp)
        logging.info(f"Successfully deployed at 'https://{webapp_url}'.")


def deploy(webapp: WebApp):
    deploy_can_build = [
        *webapp.config()['deploy'],
        config.Field(
            name='build',
            description='Build then deploy the application.',
            attending_value=False
        )
    ]
    user_config = config.load(deploy_can_build)
    webapp_url = webapp.deploy(user_config)
    return webapp_url
