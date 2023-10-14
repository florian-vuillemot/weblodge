"""
Internal utility functions for the web app.
"""
import os
import time
import logging

from dotenv import dotenv_values

from weblodge._azure import AzureWebApp, AzureService


logger = logging.getLogger('weblodge')


def get_webapp(azure_service: AzureService, subdomain: str) -> AzureWebApp:
    """
    Return a Azure Web App based on the subdomain.
    The Web App may not exists.
    """
    resource_group = azure_service.resource_groups(subdomain)
    keyvault = azure_service.keyvaults(subdomain, resource_group)
    return azure_service.web_apps(
        subdomain,
        resource_group=resource_group,
        app_service=azure_service.app_services(subdomain, resource_group),
        keyvault=keyvault
    )


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
