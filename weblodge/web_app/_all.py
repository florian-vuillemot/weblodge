"""
Delete all resources created by WebLodge.
"""
from typing import Iterable
from weblodge._azure import AzureService, AzureWebApp

from .utils import get_webapp
from .shared import WEBAPP_TAGS


def _all(azure_service: AzureService) -> Iterable[AzureWebApp]:
    """
    Return all resources with WebApp created by WebLodge.
    In case of error, the WebApp may not be exists, but other resource may exists
    and so the element is returned.
    """
    for resource_group in azure_service.resource_groups.all():
        if WEBAPP_TAGS.items() <= resource_group.tags.items():
            yield get_webapp(azure_service, resource_group.name)
