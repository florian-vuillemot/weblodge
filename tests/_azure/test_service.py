"""
Service Tests.
"""
import json
from pathlib import Path
import unittest
from unittest.mock import MagicMock

from weblodge._azure.entra import Entra
from weblodge._azure.web_app import WebApp
from weblodge._azure.resource_group import ResourceGroup
from weblodge._azure import Service, AzureWebApp
from weblodge._azure.appservice import AppService
from weblodge._azure.keyvault import KeyVault

from .cli import Cli as Cli_mocked


class TestAzureService(unittest.TestCase):
    """
    Service tests.
    """
    def test_cli(self):
        """
        Ensure the Cli is correctly instanciate.
        """
        cli = MagicMock()
        Service(cli=cli)

        # pylint: disable=protected-access
        self.assertEqual(cli, WebApp._cli)
        self.assertEqual(cli, Entra._cli)
        self.assertEqual(cli, ResourceGroup._cli)
        self.assertEqual(cli, KeyVault._cli)
        self.assertEqual(cli, AppService._cli)

    def test_all(self):
        """
        Ensure all webApp are correctly returned.
        """
        cli = Cli_mocked([
            json.loads(
                Path('./tests/_azure/api_mocks/resource_groups.json').read_text(encoding='utf-8')
            )
        ])
        service = Service(cli=cli)

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
        service = Service(cli=Cli_mocked([[]]))

        web_apps = list(service.all())
        self.assertEqual(len(web_apps), 0)

    def test_get_web_app(self):
        """
        Ensure the web app is correctly returned.
        """
        web_apps = json.loads(
            Path('./tests/_azure/api_mocks/web_apps.json').read_text(encoding='utf-8')
        )
        cli = Cli_mocked([web_apps, web_apps])
        service = Service(cli=cli)

        dev_web_app = service.get_web_app('develop')
        prod_web_app = service.get_web_app('production')

        self.assertIsInstance(dev_web_app, AzureWebApp)
        self.assertEqual(dev_web_app.name, 'develop')

        self.assertIsInstance(dev_web_app, AzureWebApp)
        self.assertEqual(prod_web_app.name, 'production')

    def test_get_free_web_app(self):
        """
        Ensure the free web app is correctly returned.
        """
        asp = json.loads(
            Path('./tests/_azure/api_mocks/appservices_plan.json').read_text(encoding='utf-8')
        )
        resource_groups = json.loads(
            Path('./tests/_azure/api_mocks/resource_groups.json').read_text(encoding='utf-8')
        )
        service = Service(
            cli=Cli_mocked([
                asp,
                resource_groups[0], # The develop resource group.
                resource_groups[1]  # The staging resource group.
            ])
        )

        free_web_app = service.get_free_web_app('northeurope')

        self.assertIsInstance(free_web_app, AzureWebApp)
        self.assertEqual(free_web_app.name, 'staging')

    def test_delete(self):
        """
        Ensure a webApp can be deleted.
        """
        cli = MagicMock()
        service = Service(cli=cli)

        service.delete('develop')
        cli.invoke.assert_called_once_with('group delete --name develop --yes', to_json=False)
