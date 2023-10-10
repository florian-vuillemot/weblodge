"""
Allow to retrieve all available tiers for a given location.
"""
from dataclasses import dataclass
import logging
from typing import List, Union

from weblodge.config import Item as ConfigItem
from weblodge._azure import AzureService, InvalidLocation

from .exceptions import CanNotFindTierLocation


logger = logging.getLogger('weblodge')


@dataclass
class WebAppTier:
    """
    Information on the WebApp hardware and price.
    """
    # Technical name of the tier.
    name: str

    # Name of the location where the tier is available.
    location: str

    # Price per hour of the tier.
    price_by_hour: float

    # Human description of the tier.
    description: str

    # Number of Cores.
    # It is a string when the SKU is free.
    cores: Union[int, str]

    # RAM in GB.
    ram: int

    # Disk size in GB.
    disk: int


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


def tiers(azure_service: AzureService, config: TiersConfig) -> List[WebAppTier]:
    """
    Return all available tiers.
    """
    try:
        return [
            WebAppTier(
                name=s.name,
                location=s.location,
                price_by_hour=s.price_by_hour,
                description=s.description,
                cores=s.cores,
                ram=s.ram,
                disk=s.disk,
            )
            for s in azure_service.app_services.skus(config.location)
        ]
    except InvalidLocation:
        raise CanNotFindTierLocation(f"Can not find any tier for the location '{config.location}'.") from InvalidLocation  # pylint: disable=line-too-long
