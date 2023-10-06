"""
Internal Azure interface.

This package is for internal use only and must not be use from a third package.
"""
from .service import Service
from .exceptions import InvalidRegion
from .interfaces import AzureService, AzureAppServiceSku, \
    AzureResourceGroup, AzureWebApp, AzureAppService, \
    AzureLogLevel, MicrosoftEntraApplication, MicrosoftEntra, \
    AzureKeyVault, AzureKeyVaultSecret
