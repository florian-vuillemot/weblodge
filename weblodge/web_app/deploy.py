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
from typing import List, Optional
from dataclasses import dataclass, field

from urllib3 import Retry, request

from weblodge.config import Item as ConfigItem
from weblodge._azure import Cli, ResourceGroup, AppService, WebApp


logger = logging.getLogger('weblodge')


@dataclass
class Deploy:
    """
    Facade to the deployment process.

    Create the infrastructure that will host the application.
    If not provide, a random name will be generated to allow user to deploy an application
    without providing any input.
    """
    # Application name.
    # This name must be unique across all of Azure WebApplication.
    # It will be used as the URL of the application and for created Azure resources.
    app_name: str = ''.join(random.choice(string.ascii_uppercase) for _ in range(20))
    # Application SKU (https://azure.microsoft.com/en-us/pricing/details/app-service/linux/).
    sku: str = 'F1'
    # Application location.
    location: str = 'northeurope'
    # Application environment.
    environment: str = 'development'
    # Dist directory containing the application zipped.
    dist: str = 'dist'

    # Infrastructure tags.
    tags: dict = field(default_factory=dict)

    @classmethod
    @property
    def config(cls) -> List[ConfigItem]:
        """
        Configure the deployment.
        """
        return [
            ConfigItem(
                name='app_name',
                description='Unique name of the application within Azure. If not provide, a random name is used.',  # pylint: disable=line-too-long
                default=cls.app_name
            ),
            ConfigItem(
                name='sku',
                description='The application computational power (https://azure.microsoft.com/en-us/pricing/details/app-service/linux/).',  # pylint: disable=line-too-long
                default=cls.sku
            ),
            ConfigItem(
                name='location',
                description='The physical application location.',
                default=cls.location
            ),
            ConfigItem(
                name='environment',
                description='The environment of your application.',
                default=cls.environment
            ),
            ConfigItem(
                name='dist',
                description='Folder containing the application zipped.',
                default=cls.dist
            ),
        ]

    def deploy(self, package_name: str='azwebapp.zip') -> Optional[str]:
        """
        Deploy the application to Azure and return its URL.
        """
        default_name = f'{self.app_name}-{self.environment}-{self.location}'

        cli = Cli()
        web_app_cls = WebApp(cli)

        logger.info('The infrastructure is being created or updated...')
        web_app = web_app_cls.create(
            self.app_name,
            AppService(cli).create(
                f'asp-{default_name}',
                self.sku,
                ResourceGroup(cli).create(
                    f'rg-{default_name}',
                    self.location,
                    tags=self.tags
                )
            )
        )
        logger.info('The infrastructure has been created or updated.')

        logger.info('Waiting the infrastructure to be running...')
        if not self.ping(web_app):
            logger.info('The infrastructure is not yet running. Retrying...')
            if not self.ping(web_app):
                logger.critical('The infrastructure is not yet running.\nPlease retry later.')
                return None
        logger.info('The infrastructure is running.')

        logger.info('Uploading the application...')
        web_app_cls.deploy(web_app, os.path.join(self.dist, package_name))
        logger.info('The application has been uploaded.')
        return web_app.host_names[0]

    def ping(self, web_app: WebApp) -> bool:
        """
        Ping the application to warm it up.
        Return True if the application is up and running.
        """
        try:
            return request(
                "GET",
                web_app.host_names[0],
                retries=Retry(total=10, backoff_factor=5)
            ).status < 400
        except:  # pylint: disable=bare-except
            return False
