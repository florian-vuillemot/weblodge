"""

"""
import logging
from typing import Iterable

from weblodge.config import Item as ConfigItem
from weblodge._azure import AzureService, AzureAppServiceSku


logger = logging.getLogger('weblodge')


class TierConfig:
    """
    Tier configuration.

    """
    items = [
        ConfigItem(
            name='location',
            description='The physical application location.',
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
        # Application location.
        self.location = location


def tiers(azure_service: AzureService, config: TierConfig) -> Iterable[AzureAppServiceSku]:
    """
    Return all available tiers.
    """
    yield from azure_service.app_services.skus(config.location)
