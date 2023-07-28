"""
Delete all resources created by WebLodge.
"""
from typing import Iterable
from weblodge._azure import ResourceGroup

from .shared import WEBAPP_TAGS


def _all() -> Iterable[ResourceGroup]:
    """
    Return all resources with WebApp created by WebLodge.
    In case of error, the WebApp may not be exists, but other resource may exists
    and so the element is returned.
    """
    for resource_group in ResourceGroup.all():
        if WEBAPP_TAGS.items() <= resource_group.tags.items():
            yield resource_group
