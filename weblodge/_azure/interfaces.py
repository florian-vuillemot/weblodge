"""
Public interface of the Azure module.
"""
from abc import abstractmethod
from typing import Dict, Iterable, Iterator


class AzureLogLevel:
    """
    Log levels.
    By default, the log level is set to Warning.
    """
    @abstractmethod
    def __init__(self) -> None:
        """
        Initialize the log level.
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

    @abstractmethod
    def to_azure(self) -> str:
        """
        Convert in Azure values.
        """


class AzureAppServiceSku:
    """
    Human representation of the SKU.
    """
    # Name of the SKU.
    name: str

    # Name of the location where the SKU is available.
    location: str

    # Price per hour of the SKU.
    price_by_hour: float

    # Human description of the SKU.
    description: str

    # Number of Cores.
    cores: int

    # RAM in GB.
    ram: int

    # Disk size in GB.
    disk: int


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

    # Current tier of the WebApp.
    tier: AzureAppServiceSku

    @abstractmethod
    def is_free(self) -> bool:
        """
        Return true if the current tier of the WebApp is free.
        """

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

    @abstractmethod
    def update(self):
        """
        Update the WebApp infrastructure.
        """


class MicrosoftEntraApplication:
    """
    Azure Application registered on the Entra platform.
    """
    client_id: str
    tenant_id: str
    subscription_id: str


class AzureService:
    """
    Allow to instanciate Azure components.
    """
    @abstractmethod
    def get_web_app(self, subdomain: str) -> AzureWebApp:
        """
        Return a WebApp.
        """

    @abstractmethod
    def get_free_web_app(self, location: str) -> AzureWebApp:
        """
        Return the existing WebApp using a free tier.
        """

    # pylint: disable=too-many-arguments
    @abstractmethod
    def get_github_application(
        self,
        subdomain: str,
        username: str,
        repository: str,
        branch: str,
        location: str
    ) -> MicrosoftEntraApplication:
        """
        Return a Azure Entra Application for a GitHub Account.
        Create the application if not exists.
        Credentials are federated based.

        :param subdomain: The application subdomain of the GitHub Application.
        :param branch: The branch of the repository that will trigger the GitHub Action.
        :param username: The username/organisation of the repository owner.
        :param repository: The name of the GitHub repository.
        :param location: The location of the application.
        :return: The Microsoft Entra representation.
        """

    @abstractmethod
    def all(self) -> Iterable[AzureWebApp]:
        """
        Return all WebApp created by WebLodge.
        """

    @abstractmethod
    def delete(self, subdomain: str) -> None:
        """
        Delete a WebApp.
        """

    @abstractmethod
    def delete_github_application(self, subdomain: str) -> None:
        """
        Delete an Azure Entra Application for a GitHub Account.

        :param subdomain: The application subdomain of the GitHub Application to delete.
        """

    @abstractmethod
    def get_skus(self, location: str) -> Iterable[AzureAppServiceSku]:
        """
        Return all available tiers.
        """

    @abstractmethod
    def log_levels(self) -> AzureLogLevel:
        """
        Return the log levels.
        """
