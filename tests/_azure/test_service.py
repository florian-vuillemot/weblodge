"""
Service Tests.
"""
import unittest

from weblodge._azure.cli import Cli
from weblodge._azure.entra import Entra
from weblodge._azure.web_app import WebApp
from weblodge._azure.log_level import LogLevel
from weblodge._azure.appservice import AppService
from weblodge._azure.keyvault import KeyVault
from weblodge._azure.resource_group import ResourceGroup
from weblodge._azure import AzureService, Service, AzureLogLevel, \
    AzureAppService, AzureResourceGroup, AzureWebApp, MicrosoftEntra, \
    AzureKeyVault


class TestAzureService(unittest.TestCase):
    """
    Service tests.
    """
    def test_service_interface(self):
        """
        Ensure the service instanciate wanted interfaces.
        """
        service = Service()

        self.assertTrue(issubclass(Service, AzureService))
        self.assertTrue(issubclass(service.resource_groups, AzureResourceGroup))
        self.assertTrue(issubclass(service.app_services, AzureAppService))
        self.assertTrue(issubclass(service.web_apps, AzureWebApp))
        self.assertTrue(issubclass(service.log_levels, AzureLogLevel))
        self.assertTrue(issubclass(service.keyvault, AzureKeyVault))
        self.assertTrue(issubclass(service.entra, MicrosoftEntra))

    def test_service_type(self):
        """
        Ensure the service instanciate wanted types.
        """
        service = Service()

        self.assertIsInstance(service, AzureService)
        self.assertEqual(service.resource_groups, ResourceGroup)
        self.assertEqual(service.app_services, AppService)
        self.assertEqual(service.web_apps, WebApp)
        self.assertEqual(service.log_levels, LogLevel)
        self.assertEqual(service.keyvault, KeyVault)
        self.assertEqual(service.entra, Entra)

    def test_cli(self):
        """
        Ensure the Cli is correctly instanciate.
        """
        service = Service()

        # pylint: disable=protected-access
        self.assertIsInstance(service.resource_groups._cli, Cli)
        self.assertIsInstance(service.app_services._cli, Cli)
        self.assertIsInstance(service.web_apps._cli, Cli)
        self.assertIsInstance(service.keyvault._cli, Cli)
        self.assertIsInstance(service.entra._cli, Cli)

        # pylint: disable=protected-access
        self.assertEqual(service.cli, service.resource_groups._cli)
        self.assertEqual(service.cli, service.app_services._cli)
        self.assertEqual(service.cli, service.web_apps._cli)
        self.assertEqual(service.cli, service.keyvault._cli)
        self.assertEqual(service.cli, service.entra._cli)
