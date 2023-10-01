"""
Test the WebApp.
"""
import json
from pathlib import Path
import unittest
from unittest.mock import MagicMock

from weblodge.web_app import WebApp
from weblodge.parameters import Parser
from weblodge._azure import Service, sku
from weblodge._azure.exceptions import InvalidSku


class TestWebApp(unittest.TestCase):
    """
    Test the WebApp facade.
    """
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
        self.assertEqual(len(list(tiers)), 12)

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
        self.assertEqual(len(list(tiers)), 12)
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
        tiers = web_app.tiers({})

        with self.assertRaises(InvalidSku):
            next(tiers)
