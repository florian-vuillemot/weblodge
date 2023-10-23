"""
Internal utility functions for the web app.
"""
import os
import time
import logging

from dotenv import dotenv_values

from weblodge._azure import AzureWebApp


logger = logging.getLogger('weblodge')


def set_webapp_env_var(webapp: AzureWebApp, env_file: str, env_update_waiting_time: int) -> None:
    """
    Udpate a Web App environment variable.
    """
    if os.path.exists(env_file):
        logger.info(f"Updating the environment variable with '{env_file}'...")
        env = dotenv_values(env_file)
        webapp.update_environment(env)
        logger.info('Environment variable updated.')
        logger.info('Waiting the application to restart...')
        time.sleep(env_update_waiting_time)
    else:
        logger.info('No environment file found.')
