"""
Public interface of the Azure module.
"""
from typing import Dict, Iterable, Iterator, List, Optional
from abc import abstractmethod


class AzureLogLevel:
    """
    Log levels.
    By default, the log level is set to Warning.
    """
    @abstractmethod
    def error(self) -> None:
        """
        Set the log level to error.
        """

    @abstractmethod
    def information(self) -> None:
        """
        Set the log level to information.
        """

    @abstractmethod
    def verbose(self) -> None:
        """
        Set the log level to verbose.
        """

    @abstractmethod
    def warning(self) -> None:
        """
        Set the log level to warning.
        """


class AzureResourceGroup:
    """
    Azure Resource Group.
    """
    # Name of the Resource Group.
    name: str

    # Location of the Resouce Group.
    location: str

    # Tags of the Resource Group.
    tags: Dict[str, str]

    @abstractmethod
    def create(self, location: str, tags: Dict[str, str] = None) -> 'AzureResourceGroup':
        """
        Create a new Resource Group and return it.
        """

    @abstractmethod
    def delete(self) -> None:
        """
        Delete the resource group.
        """

    @classmethod
    @abstractmethod
    def all(cls) -> Iterator['AzureResourceGroup']:
        """
        Return all the WebApps.
        """


class AzureAppService:
    """
    Azure AppService Plan.
    """
    # Name of the Resource Group.
    name: str

    # Location of the Resouce Group.
    location: str

    # Tags of the Resource Group.
    tags: Dict[str, str]

    # True if the AppService Plan support AlwaysOn.
    always_on_supported: bool

    # True if the AppService Plan is Free.
    is_free: bool

    # List of supported SKUs.
    skus = []

    @abstractmethod
    def create(self, sku: str) -> 'AzureAppService':
        """
        Create a Linux AppService with Python.
        """

    @classmethod
    @abstractmethod
    def all(cls) -> Iterator['AzureAppService']:
        """
        Return all the AppService.
        """

    @classmethod
    @abstractmethod
    def get_existing_free(cls, location: str) -> Optional['AzureAppService']:
        """
        Return the free existing Azure App Service if exists in that location.
        None otherwise.
        """


class AzureWebApp:
    """
    Azure Web App.
    """
    # Name of the WebApp.
    # It is also its unique subdomain on Azure.
    name: str

    # The WebApp location.
    # Ex: northeurope, westeurope, etc.
    location: str

    # WebApp domain.
    # Ex: weblodge.azurewebsites.net
    domain: str

    # Tags of the Web App.
    tags: Dict[str, str]

    # Azure App Service of the WebApp.
    app_service: AzureAppService

    # Azure Resource Group of the WebApp.
    resource_group: AzureResourceGroup

    @abstractmethod
    def create(self) -> 'AzureWebApp':
        """
        Create the WebApp.
        """

    @abstractmethod
    def exists(self) -> bool:
        """
        Return True if the Web App exists.
        False otherwise.
        """

    @classmethod
    @abstractmethod
    def all(cls) -> Iterator['AzureWebApp']:
        """
        Return all the WebApps.
        """

    @abstractmethod
    def set_log_level(self, log_level: AzureLogLevel) -> None:
        """
        Set the WebApp log level.
        """

    @abstractmethod
    def deploy(self, src: str) -> None:
        """
        Deploy an application zipped.
        """

    @abstractmethod
    def logs(self) -> None:
        """
        Stream WebApp logs.
        This is a blocking operation. User must run CTRL+C to stop the process.
        """

    @abstractmethod
    def update_environment(self, env: Dict) -> None:
        """
        Update the WebApp environment variables.
        """

    @abstractmethod
    def deployment_in_progress(self) -> bool:
        """
        True if the WebApp is deploying.
        """

    @abstractmethod
    def restart(self) -> None:
        """
        Restart the WebApp.
        """


class AzureKeyVaultSecret:
    # Secret name.
    name: str

    # Secret value.
    value: str

    # Secret URI.
    uri: str


class AzureKeyVault:
    """
    Azure KeyVault representation.
    """
    # The KeyVault name.
    name: str

    # It's resource group.
    resource_group: AzureResourceGroup

    # Tags of the KeyVault.
    tags: Dict[str, str]

    @abstractmethod
    def __init__(self, name: str, resource_group: AzureResourceGroup):
        """
        Initialize the KeyVault.
        """

    @abstractmethod
    def create(self) -> 'AzureKeyVault':
        """
        Create the Azure KeyVault.
        """

    @abstractmethod
    def delete(self) -> None:
        """
        Delete the Azure KeyVault.
        """

    @abstractmethod
    def exists(self) -> bool:
        """
        Return True if the Key Vault exists.
        False otherwise.
        """

    @abstractmethod
    def get_all(self) -> Iterable[AzureKeyVaultSecret]:
        """
        Return the KeyVault secrets.
        """

    @abstractmethod
    def set(self, name: str, value: str) -> AzureKeyVaultSecret:
        """
        Create a secret.
        """


class MicrosoftEntraApplication:
    """
    Azure Application registered on the Entra platform.
    """
    client_id: str
    tenant_id: str
    subscription_id: str


class MicrosoftEntra:
    """
    Allow to create Azure Entra Applications.
    """
    # pylint: disable=too-many-arguments
    @classmethod
    @abstractmethod
    def github_application(
        cls,
        name: str,
        username: str,
        repository: str,
        branch: str,
        resource_group: AzureResourceGroup
    ) -> MicrosoftEntraApplication:
        """
        Return a Azure Entra Application for a GitHub Account.
        Credentials are federated based.

        :param name: The name of the GitHub Application.
        :param branch: The branch of the repository that will trigger the GitHub Action.
        :param username: The username/organisation of the repository owner.
        :param repository: The name of the GitHub repository.
        :param resource_group: The resource group where the application will be deployed. Must exists.
        :return: The Microsoft Entra representation.
        """


class AzureService:
    """
    Allow to instanciate Azure components.
    """
    resource_groups: AzureResourceGroup
    app_services: AzureAppService
    web_apps: AzureWebApp
    log_levels: AzureLogLevel
    keyvault: AzureKeyVault
    entra: MicrosoftEntra
