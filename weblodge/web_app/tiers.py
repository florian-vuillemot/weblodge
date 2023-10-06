"""
Allow to retrieve all available tiers for a given location.
"""
import logging
from typing import List

from weblodge.config import Item as ConfigItem
from weblodge._azure import AzureService, AzureAppServiceSku, InvalidRegion

from .exceptions import CanNotFindTierLocation


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


def tiers(azure_service: AzureService, config: TiersConfig) -> List[AzureAppServiceSku]:
    """
    Return all available tiers.
    """
    try:
        return list(azure_service.app_services.skus(config.location))
    except InvalidRegion:
        raise CanNotFindTierLocation(f"Can not find any tier for the location '{config.location}'.") from InvalidRegion
