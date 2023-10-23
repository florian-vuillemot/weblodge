"""
Service Tests.
"""
import json
from pathlib import Path
import unittest

from weblodge._azure.cli import Cli
from weblodge._azure.entra import Entra
from weblodge._azure.web_app import WebApp
from weblodge._azure.log_level import LogLevel
from weblodge._azure.resource_group import ResourceGroup
from weblodge._azure import AzureService, Service, AzureLogLevel, AzureWebApp, MicrosoftEntra

from .cli import Cli as Cli_mocked


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
        self.assertTrue(issubclass(service.web_apps, AzureWebApp))
        self.assertTrue(issubclass(service.log_levels, AzureLogLevel))
        self.assertTrue(issubclass(service.entra, MicrosoftEntra))

    def test_service_type(self):
        """
        Ensure the service instanciate wanted types.
        """
        service = Service()

        self.assertIsInstance(service, AzureService)
        self.assertEqual(service.web_apps, WebApp)
        self.assertEqual(service.log_levels, LogLevel)
        self.assertEqual(service.entra, Entra)

    def test_cli(self):
        """
        Ensure the Cli is correctly instanciate.
        """
        service = Service()

        # pylint: disable=protected-access
        self.assertIsInstance(service.web_apps._cli, Cli)
        self.assertIsInstance(service.entra._cli, Cli)

        # pylint: disable=protected-access
        self.assertEqual(service.cli, service.web_apps._cli)
        self.assertEqual(service.cli, service.entra._cli)

    def test_all(self):
        """
        Ensure all webApp are correctly returned.
        """
        cli = Cli_mocked([
            json.loads(
                Path('./tests/_azure/api_mocks/resource_groups.json').read_text(encoding='utf-8')
            )
        ])
        ResourceGroup.set_cli(cli)

        service = Service()

        web_apps = list(service.all())

        self.assertEqual(len(web_apps), 3)

        self.assertIsInstance(web_apps[0], AzureWebApp)
        self.assertIsInstance(web_apps[1], AzureWebApp)
        self.assertIsInstance(web_apps[2], AzureWebApp)

        self.assertEqual(web_apps[0].name, 'develop')
        self.assertEqual(web_apps[1].name, 'staging')
        self.assertEqual(web_apps[2].name, 'production')

    def test_no_web_app(self):
        """
        Ensure the behaviours when there is no web app.
        """
        ResourceGroup.set_cli(Cli_mocked([[]]))

        service = Service()

        web_apps = list(service.all())
        self.assertEqual(len(web_apps), 0)
