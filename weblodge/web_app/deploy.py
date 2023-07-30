"""
Create the infrastructure that will host the application.

The infrastructure is composed of:
- Resource Group
- App Service Plan
- Web App

All that infrastructure is created in the same Azure region and in the same Azure
Resource Group.
"""
import os
import random
import string
import logging

from weblodge.config import Item as ConfigItem
from weblodge._azure import WebApp as AzureWebApp

from .shared import WEBAPP_TAGS
from .exceptions import FreeApplicationAlreadyDeployed
from .utils import get_webapp, set_webapp_env_var, get_free_web_app


logger = logging.getLogger('weblodge')


class DeploymentConfig:
    """
    Deployment configuration.

    Configuration of the infrastructure that will host the application.
    If not provide, a random name will be generated to allow user to deploy an application
    without providing any input.
    """
    # Zip file that contains the user application code.
    package: str = 'azwebapp.zip'

    # Configurable items of the deployment.
    items = [
        ConfigItem(
            name='subdomain',
            description='Unique subdomain of the application within Azure. If not provide, a random subdomain is used.',  # pylint: disable=line-too-long
            default=''.join(random.choice(string.ascii_lowercase) for _ in range(20))
        ),
        ConfigItem(
            name='sku',
            description='The application computational power (https://azure.microsoft.com/en-us/pricing/details/app-service/linux/).',  # pylint: disable=line-too-long
            default='F1'
        ),
        ConfigItem(
            name='location',
            description='The physical application location.',
            default='northeurope'
        ),
        ConfigItem(
            name='environment',
            description='The environment of your application.',
            default='production'
        ),
        ConfigItem(
            name='dist',
            description='Folder containing the application zipped.',
            default='dist'
        ),
        ConfigItem(
            name='env_file',
            description='The file containing the environment variable.',
            default='.env'
        ),
    ]

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            subdomain,
            sku,
            location,
            environment,
            dist,
            env_file,
            *_args,
            **_kwargs
        ):
        # Application subdomain.
        # This name must be unique across all of Azure WebApplication.
        # It will be used as the URL of the application and for created Azure resources.
        self.subdomain = subdomain
        # Application SKU (https://azure.microsoft.com/en-us/pricing/details/app-service/linux/).
        self.sku = sku
        # Application location.
        self.location = location
        # Application environment.
        self.environment = environment
        # Dist directory containing the application zipped.
        self.dist = dist
        # File containing environment variables.
        self.env_file = env_file

        # Infrastructure tags.
        self.tags = {
            'environment': self.environment
        }


def deploy(config: DeploymentConfig) -> AzureWebApp:
    """
    Deploy the application to Azure and return its URL.
    """
    web_app = get_webapp(config.subdomain)

    if not web_app.exists():
        logger.info('The infrastructure is being created...')
        if not web_app.app_service.exists():
            if config.sku == 'F1':
                # Only one free AppService Plan is allowed per Azure subscription and location.
                # Check if a free AppService Plan already exists.
                if free_web_app := get_free_web_app(config.location):
                    logger.info('Stopping the deployment. No infrastructure created.')
                    raise FreeApplicationAlreadyDeployed(free_web_app.name)
            if not web_app.resource_group.exists():
                web_app.resource_group.create(
                    location=config.location,
                    tags={
                        **config.tags,
                        **WEBAPP_TAGS
                    }
                )
            web_app.app_service.create(config.sku)
        web_app.create()
        logger.info('The infrastructure is created.')

    set_webapp_env_var(web_app, config.env_file)

    logger.info('Uploading the application...')
    web_app.deploy(os.path.join(config.dist, config.package))
    logger.info('The application has been uploaded.')

    return web_app
