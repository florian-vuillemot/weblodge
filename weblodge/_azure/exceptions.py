"""
Module exceptions.
"""

class AzureException(Exception):
    """
    Base class for all Azure exceptions.
    """

class CanLoadResource(AzureException):
    """
    Raise when a resource cannot be loaded from Azure.
    """

class ResourceNotFound(AzureException):
    """
    Raise when a resource cannot be found on Azure.
    """

class CliNotSet(AzureException):
    """
    Raise when the Azure CLI is not set.
    """

class ResourceGroupNotFound(ResourceNotFound):
    """
    Raise when a resource group cannot be found on Azure.
    """

class AppServiceNotFound(ResourceNotFound):
    """
    Raise when an app service plan cannot be found on Azure.
    """

class CLIException(AzureException):
    """
    Raise when an error occurs while executing an Azure CLI command.
    """

class InvalidSku(AzureException):
    """
    Raise when an invalid SKU is provided.
    """

class InvalidLocation(AzureException):
    """
    Raise when an invalid  is provided.
    """

class SecretNotFound(AzureException):
    """
    Raise when a secret on a KeyVault cannot be found.
    """

class CanNotChangeTheResourceLocation(AzureException):
    """
    Raise when a resource location cannot be changed.
    """
