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
from typing import List
from dataclasses import dataclass, field

from weblodge.config import Item as ConfigItem
from weblodge._azure import Cli, ResourceGroup, AppService, WebApp


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

    def deploy(self, package_name: str='azwebapp.zip') -> str:
        """
        Deploy the application to Azure and return its URL.
        """
        default_name = f'{self.app_name}-{self.environment}-{self.location}'

        cli = Cli()
        web_app_cls = WebApp(cli)

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

        web_app_cls.deploy(web_app, os.path.join(self.dist, package_name))
        return web_app.host_names[0]
