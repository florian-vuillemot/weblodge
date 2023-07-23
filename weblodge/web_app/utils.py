"""
Internal utility functions for the web app.
"""
import os
import logging

from dotenv import dotenv_values

from weblodge._azure import WebApp as AzureWebApp, AppService as AzureAppService, ResourceGroup as AzureResourceGroup


logger = logging.getLogger('weblodge')


def get_webapp(subdomain: str) -> AzureWebApp:
    """
    Return a Azure Web App based on the subdomain.
    The Web App may not exists.
    """
    resource_group = AzureResourceGroup(subdomain)
    return AzureWebApp(
        subdomain,
        resource_group=resource_group,
        app_service=AzureAppService(subdomain, resource_group)
    )


def set_webapp_env_var(webapp: AzureWebApp, env_file: str) -> bool:
    """
    Udpate a Web App environment variable.
    Return True if the environment variable has been updated, False otherwise.
    """
    if os.path.exists(env_file):
        logger.info(f"Updating the environment variable with '{env_file}'...")
        env = dotenv_values(env_file)
        webapp.update_environment(env)
        logger.info('Environment variable updated.')
        return

    logger.info('No environment file found.')
