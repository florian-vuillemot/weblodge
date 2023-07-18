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
from weblodge._azure import ResourceGroup, AppService, WebApp as AzureWebApp


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
            name='app_name',
            description='Unique name of the application within Azure. If not provide, a random name is used.',  # pylint: disable=line-too-long
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
    ]

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            app_name,
            sku,
            location,
            environment,
            dist,
            *_args,
            **_kwargs
        ):
        # Application name.
        # This name must be unique across all of Azure WebApplication.
        # It will be used as the URL of the application and for created Azure resources.
        self.app_name = app_name
        # Application SKU (https://azure.microsoft.com/en-us/pricing/details/app-service/linux/).
        self.sku = sku
        # Application location.
        self.location = location
        # Application environment.
        self.environment = environment
        # Dist directory containing the application zipped.
        self.dist = dist

        # Infrastructure tags.
        self.tags = {
            'environment': self.environment,
            'managed-by': 'weblodge'
        }


def deploy(config: DeploymentConfig) -> AzureWebApp:
    """
    Deploy the application to Azure and return its URL.
    """
    resource_group = ResourceGroup(config.app_name)
    asp_service = AppService(config.app_name, resource_group)
    web_app = AzureWebApp(config.app_name, resource_group, asp_service)

    if not web_app.exists():
        logger.info('The infrastructure is being created...')
        if not asp_service.exists():
            if not resource_group.exists():
                resource_group.create(location=config.location, tags=config.tags)
            asp_service.create(config.sku)
        web_app.create()
        logger.info('The infrastructure is created.')

    logger.info('Uploading the application...')
    web_app.deploy(os.path.join(config.dist, config.package))
    logger.info('The application has been uploaded.')

    return web_app
