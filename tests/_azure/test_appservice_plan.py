"""
App Service Plan Tests.
"""
import json
from pathlib import Path
import unittest
from unittest.mock import MagicMock

from weblodge._azure import sku
from weblodge._azure.appservice import AppService, ResourceGroup, InvalidSku

from .cli import Cli


class TestAppService(unittest.TestCase):
    """
    App Service tests.
    """
    def setUp(self) -> None:
        self.app_services = json.loads(
            Path('./tests/_azure/api_mocks/appservices_plan.json').read_text(encoding='utf-8')
        )
        self.resource_group = json.loads(
            Path('./tests/_azure/api_mocks/resource_groups.json').read_text(encoding='utf-8')
        )[0]
        self.skus = json.loads(
            Path('./tests/_azure/api_mocks/skus.json').read_text(encoding='utf-8')
        )
        return super().setUp()

    def test_create(self):
        """
        Test the create.
        """
        expected_output = self.app_services[0]

        resource_group = ResourceGroup(name=expected_output['resourceGroup'], from_az=self.resource_group)
        app_service = AppService(
            name=expected_output['name'],
            resource_group=resource_group
        )
        app_service.set_cli(Cli([expected_output, expected_output]))
        app_service.sku = 'B1'
        app_service = app_service.create()

        self.assertEqual(app_service.name, expected_output['name'])
        self.assertEqual(app_service.id_, expected_output['id'])

    def test_always_on_supported(self):
        """
        Test the always_on_supported property.
        """
        expected_output = self.app_services[0]

        resource_group = ResourceGroup(name=expected_output['resourceGroup'])
        app_service = AppService(
            name=expected_output['name'],
            resource_group=resource_group
        )
        app_service.set_cli(Cli(expected_output))

        self.assertTrue(app_service.always_on_supported)

    def test_always_on_not_supported(self):
        """
        Test the always_on_supported property.
        """
        expected_output = self.app_services[1]

        resource_group = ResourceGroup(name=expected_output['resourceGroup'])
        app_service = AppService(
            name=expected_output['name'],
            resource_group=resource_group,
        )
        app_service.set_cli(Cli(expected_output))

        self.assertFalse(app_service.always_on_supported)

    def test_set_sku(self):
        """
        Set the SKU.
        """
        sku.REQUEST = MagicMock()
        sku.REQUEST.return_value.json.return_value = self.skus

        resource_group = MagicMock(location='westeurope')
        asp = AppService(name='test', resource_group=resource_group)

        asp.sku = 'B1'

        self.assertEqual(asp.sku.name, 'B1')  # pylint: disable=no-member
        self.assertFalse(asp.is_free)
        self.assertTrue(asp.always_on_supported)

        asp.sku = 'F1'

        self.assertEqual(asp.sku.name, 'F1')  # pylint: disable=no-member
        self.assertTrue(asp.is_free)
        self.assertFalse(asp.always_on_supported)

    def test_set_invalid_sku(self):
        """
        Set a invalid SKU and verify raised.
        """
        asp = AppService(name='test', resource_group=None)

        with self.assertRaises(InvalidSku):
            asp.sku = 'Invalid SKU'

    def test_is_free(self):
        """
        Test if AppService is free.
        """
        is_not_free = AppService(
            name='app_service',
            resource_group=ResourceGroup(name='rg'),
            from_az={
                "sku": {
                    "capabilities": None,
                    "capacity": 1,
                    "family": "Pv3",
                    "locations": None,
                    "name": "P1v3",
                    "size": "P1v3",
                    "skuCapacity": None,
                    "tier": "PremiumV3"
                },
                "tags": {"managedby": "weblodge"},
            }
        )

        self.assertFalse(is_not_free.is_free)

        is_free = AppService(
            name='app_service',
            resource_group=ResourceGroup(name='rg'),
            from_az={
                "sku": {
                    "capabilities": None,
                    "capacity": 1,
                    "family": "Shared",
                    "locations": None,
                    "name": "F1",
                    "size": "F2",
                    "skuCapacity": None,
                    "tier": "Shared"
                },
                "tags": {"managedby": "weblodge"},
            }
        )

        self.assertTrue(is_free.is_free)
