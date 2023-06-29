import logging

from weblodge.config import Config
from weblodge.web_app import WebApp


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def main():
    c = Config()
    w = WebApp(c)

    if c.action == 'build':
        logging.info('Building...')
        c.load(w.config()['build'])
        w.build()
        logging.info('Successfully built.')
    elif c.action == 'deploy':
        logging.info('Deploying...')
        c.load(w.config()['deploy'])
        webapp_url = w.deploy()
        logging.info(f"Successfully deployed at 'https://{webapp_url}'.")
