"""
Test the WebApp facade.
"""
import json
from pathlib import Path
import unittest
from unittest.mock import MagicMock

from weblodge._azure import sku

from weblodge._azure import Service
from weblodge._azure.interfaces import AzureAppServiceSku
from weblodge.parameters import Parser
from weblodge._azure.exceptions import InvalidSku
from weblodge.web_app import WebApp, CanNotFindTierLocation
from weblodge.web_app.deploy import DeploymentConfig
from weblodge.web_app.exceptions import InvalidTier


class TestWebApp(unittest.TestCase):
    """
    Test the WebApp facade.
    """
    def setUp(self) -> None:
        DeploymentConfig.env_update_waiting_time = 0

        self.f1_tier = AzureAppServiceSku()
        self.f1_tier.name = 'F1'
        self.f1_tier.location = 'westeurope'
        self.f1_tier.price_by_hour = 0.05
        self.f1_tier.description = 'Free'
        self.f1_tier.cores = 1
        self.f1_tier.ram = 1
        self.f1_tier.disk = 1

        self.s1_tier = AzureAppServiceSku()
        self.s1_tier.name = 'S1'
        self.s1_tier.location = 'westeurope'
        self.s1_tier.price_by_hour = 0.05
        self.s1_tier.description = 'Free'
        self.s1_tier.cores = 1
        self.s1_tier.ram = 1
        self.s1_tier.disk = 1

        return super().setUp()

    def test_tiers_default(self):
        """
        Test the tiers command.
        """
        sku.REQUEST = MagicMock()
        skus = json.loads(
            Path('./tests/_azure/api_mocks/skus.json').read_text(encoding='utf-8')
        )

        sku.REQUEST.return_value.json.return_value = skus

        web_app = WebApp(Parser().load, Service())
        tiers = web_app.tiers({})
        self.assertEqual(len(tiers), 12)

    def test_tiers_with_location(self):
        """
        Test the tiers command with a location.
        """
        sku.REQUEST = MagicMock()
        sku.RETRY = MagicMock()

        skus = json.loads(
            Path('./tests/_azure/api_mocks/skus.json').read_text(encoding='utf-8')
        )

        sku.RETRY.return_value = 42
        sku.REQUEST.return_value.json.return_value = skus

        web_app = WebApp(Parser().load, Service())
        tiers = web_app.tiers({'location': 'westeurope'})
        self.assertEqual(len(tiers), 12)
        sku.REQUEST.assert_called_with(
            'GET',
            "https://prices.azure.com/api/retail/prices?$filter=serviceName eq 'Azure App Service' and contains(productName, 'Linux') and armRegionName eq 'westeurope' and unitOfMeasure eq '1 Hour' and type eq 'Consumption' and isPrimaryMeterRegion eq true and currencyCode eq 'USD'",  # pylint: disable=line-too-long
            retries=42
        )

    def test_tiers_raise(self):
        """
        Test the tiers command when API failed.
        """
        sku.REQUEST = None

        web_app = WebApp(Parser().load, Service())

        with self.assertRaises(InvalidSku):
            web_app.tiers({})

    def test_tiers_invalid_location(self):
        """
        Test the tiers command when API failed.
        """
        sku.REQUEST = MagicMock()
        sku.REQUEST.return_value.json.return_value = {'Items': []}

        web_app = WebApp(Parser().load, Service())

        with self.assertRaises(CanNotFindTierLocation):
            web_app.tiers({})

    def test_deploy(self):
        """
        Test the deploy operation.
        """
        azure_service = MagicMock()
        azure_service.app_services.skus.return_value = [self.s1_tier, self.f1_tier]
        azure_service.web_apps.exists.return_value = True
        web_app = WebApp(Parser().load, azure_service)
        success, config, tier = web_app.deploy({})

        self.assertTrue(success)
        self.assertEqual(config['location'], 'northeurope')
        self.assertEqual(config['tier'], 'F1')

        self.assertEqual(tier.name, self.f1_tier.name)
        self.assertEqual(tier.location, self.f1_tier.location)
        self.assertEqual(tier.price_by_hour, self.f1_tier.price_by_hour)
        self.assertEqual(tier.description, self.f1_tier.description)
        self.assertEqual(tier.cores, self.f1_tier.cores)
        self.assertEqual(tier.ram, self.f1_tier.ram)
        self.assertEqual(tier.disk, self.f1_tier.disk)

    def test_deploy_config(self):
        """
        Test the deploy operation with configuration.
        """
        azure_service = MagicMock()
        azure_service.app_services.skus.return_value = [self.s1_tier, self.f1_tier]
        azure_service.web_apps.exists.return_value = True
        web_app = WebApp(Parser().load, azure_service)
        success, config, tier = web_app.deploy({
            'tier': 'S1',
            'location': 'westeurope'
        })

        self.assertTrue(success)
        self.assertEqual(config['location'], 'westeurope')
        self.assertEqual(config['tier'], 'S1')

        self.assertEqual(tier.name, self.s1_tier.name)
        self.assertEqual(tier.location, self.s1_tier.location)
        self.assertEqual(tier.price_by_hour, self.s1_tier.price_by_hour)
        self.assertEqual(tier.description, self.s1_tier.description)
        self.assertEqual(tier.cores, self.s1_tier.cores)
        self.assertEqual(tier.ram, self.s1_tier.ram)
        self.assertEqual(tier.disk, self.s1_tier.disk)

    def test_deploy_invalid_tier(self):
        """
        Ensure an exception is raised when the tier is invalid.
        """
        azure_service = MagicMock()
        azure_service.app_services.skus.return_value = [self.s1_tier, self.f1_tier]
        azure_service.web_apps.exists.return_value = True
        web_app = WebApp(Parser().load, azure_service)

        with self.assertRaises(InvalidTier):
            web_app.deploy({'tier': 'invalid'})
