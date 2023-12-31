"""
Wrapper around Azure Web App components and settings.
"""
from .web_app import WebApp
from .exceptions import NoMoreFreeApplicationAvailable, CanNotFindTierLocation, InvalidTier
