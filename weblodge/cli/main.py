import logging

from weblodge.config import Config
from weblodge.web_app import WebApp


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def main():
    c = Config()
    w = WebApp(c)

    if c.action == 'build':
        logging.info('Starting WebApp build.')
        c.load(w.config()['build'])
        w.build()
        logging.info('WebApp built successfully.')
    elif c.action == 'deploy':
        logging.info('Starting WebApp deployment.')
        c.load(w.config()['deploy'])
        webapp_url = w.deploy()
        logging.info(f"WebApp deployed successfully at 'https://{webapp_url}'.")
