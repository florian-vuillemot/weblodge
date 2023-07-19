"""
App Service Plan Tests.
"""
import json
from pathlib import Path
import unittest

from weblodge._azure import AppService, ResourceGroup

from .cli import Cli


class TestAppService(unittest.TestCase):
    """
    App Service tests.
    """
    def setUp(self) -> None:
        self.app_services = json.loads(
            Path('./tests/_azure/api_mocks/appservices_plan.json').read_text(encoding='utf-8')
        )
        return super().setUp()

    def test_create(self):
        """
        Test the create.
        """
        expected_output = self.app_services[0]

        resource_group = ResourceGroup(name=expected_output['resourceGroup'], cli=None)
        app_service = AppService(
            name=expected_output['name'],
            resource_group=resource_group,
            cli=Cli(expected_output)
        )

        self.assertEqual(app_service.name, expected_output['name'])
        self.assertEqual(app_service.id_, expected_output['id'])

    def test_always_on_supported(self):
        """
        Test the always_on_supported property.
        """
        expected_output = self.app_services[0]

        resource_group = ResourceGroup(name=expected_output['resourceGroup'], cli=None)
        app_service = AppService(
            name=expected_output['name'],
            resource_group=resource_group,
            cli=Cli(expected_output)
        )

        self.assertTrue(app_service.always_on_supported)

    def test_always_on_not_supported(self):
        """
        Test the always_on_supported property.
        """
        expected_output = self.app_services[1]

        resource_group = ResourceGroup(name=expected_output['resourceGroup'], cli=None)
        app_service = AppService(
            name=expected_output['name'],
            resource_group=resource_group,
            cli=Cli(expected_output)
        )

        self.assertFalse(app_service.always_on_supported)