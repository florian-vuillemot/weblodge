"""
Allow to retrieve all available tiers for a given location.
"""
import logging
from typing import Iterable

from weblodge.config import Item as ConfigItem
from weblodge._azure import AzureService, AzureAppServiceSku


logger = logging.getLogger('weblodge')


class TiersConfig:
    """
    Tiers configuration.

    Tier or "SKU" on Azure is the name of the plan that will be used to host the application.
    It come with a price and hardware capabilities that may be asked by the user.
    """
    items = [
        ConfigItem(
            name='location',
            description='The physical location of tiers.',
            default='northeurope'
        ),
    ]

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            location,
            *_args,
            **_kwargs
        ):
        # Tiers location.
        self.location = location


def tiers(azure_service: AzureService, config: TiersConfig) -> Iterable[AzureAppServiceSku]:
    """
    Return all available tiers.
    """
    yield from azure_service.app_services.skus(config.location)
