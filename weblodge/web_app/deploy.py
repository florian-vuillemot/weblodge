import os
import random
import string
from typing import List
from dataclasses import dataclass, field

from weblodge.config import Item as ConfigItem
from weblodge._azure import Cli, ResourceGroup, AppService, WebApp


@dataclass
class Deploy:
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
        Configure the application.
        """
        return [
            ConfigItem(
                name='app_name',
                description='The unique name of the application. If not provide, a random name will be generated.',
                default=cls.app_name
            ),
            ConfigItem(
                name='sku',
                description='The application computational power (https://azure.microsoft.com/en-us/pricing/details/app-service/linux/).',
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
        print(default_name)
        cli = Cli()
        rg = ResourceGroup(cli)
        wa = WebApp(cli)
        ap = AppService(cli)

        _rg = rg.create(f'rg-{default_name}', self.location, self.tags)
        _ap = ap.create(f'asp-{default_name}', self.sku, _rg)
        _wa = wa.create(self.app_name, _ap)

        wa.deploy(_wa, os.path.join(self.dist, package_name))
        return _wa.host_names[0]
