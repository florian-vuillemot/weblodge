import os
import random
import string
from typing import List
from dataclasses import dataclass, field

from u_deploy.config import ConfigField
from u_deploy._azure import Cli, ResourceGroup, AppService, WebApp


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

    @classmethod
    def config(cls) -> List[ConfigField]:
        """
        Configure the application.
        """
        return [
            ConfigField(
                name='app-name',
                description='The unique name of the application. If not provide, a random name will be generated.',
                example='my-app',
                default=cls.app_name
            ),
            ConfigField(
                name='sku',
                description='The application SLU (https://azure.microsoft.com/en-us/pricing/details/app-service/linux/).',
                example='F1, B1',
                default=cls.sku
            ),
            ConfigField(
                name='location',
                description='The physical application location.',
                example='northeurope, westeurope',
                default=cls.location
            ),
            ConfigField(
                name='environment',
                description='The environment of your application.',
                example='production, staging, development',
                default=cls.environment
            ),
            ConfigField(
                name='dist',
                description='Folder containing the application zipped.',
                example='dist',
                default=cls.dist
            ),
        ]

    def deploy(self, package_name: str='azwebapp.zip') -> None:
        """
        Deploy the application to Azure.
        """
        default_name = f'{self.app_name}-{self.environment}-{self.location}'
        cli = Cli()
        rg = ResourceGroup(cli)
        wa = WebApp(cli)
        ap = AppService(cli)

        _rg = rg.create(f'rg-{default_name}', self.location)
        _ap = ap.create(f'asp-{default_name}', self.sku, _rg)
        _wa = wa.create(self.app_name, _ap)

        wa.deploy(_wa, os.path.join(self.dist, package_name))
        return _wa.host_names[0]
