import os
import random
import string
from typing import List
from dataclasses import dataclass, field

from weblodge.config import Item as ConfigItem
from weblodge._azure import Cli, ResourceGroup, AppService, WebApp


@dataclass
class Delete:
    # Application name to delete.
    app_name: str = None

    @classmethod
    @property
    def config(cls) -> List[ConfigItem]:
        """
        Configure the application.
        """
        return [
            ConfigItem(
                name='app_name',
                description='The application name to delete.',
                default=cls.app_name
            )
        ]

    def delete(self) -> None:
        """
        Delete the application and each Azure resources.
        """
        cli = Cli()
        rg = ResourceGroup(cli)
        wa = WebApp(cli)

        _wa = wa.get(self.app_name)
        rg.delete(_wa.resource_group)
