"""
Tests SKU internal API.
"""
import json
import unittest
from pathlib import Path
from unittest.mock import MagicMock

from weblodge._azure import sku
from weblodge._azure.exceptions import InvalidSku


class TestSku(unittest.TestCase):
    """
    Tests SKU internal API.
    """
    def setUp(self) -> None:
        self.skus = json.loads(
            Path('./tests/_azure/api_mocks/skus.json').read_text(encoding='utf-8')
        )
        return super().setUp()

    def test_default(self):
        """
        Ensure SKU is properly setted.
        """
        sku.REQUEST = MagicMock()
        sku.REQUEST.return_value.json.return_value = self.skus

        sku.RETRY = MagicMock()
        sku.RETRY.return_value = 42

        skus = list(sku.get_skus('northeurope'))

        self.assertEqual(len(skus), 12)
        sku.REQUEST.assert_called_with(
            'GET',
            "https://prices.azure.com/api/retail/prices?$filter=serviceName eq 'Azure App Service' and contains(productName, 'Linux') and armRegionName eq 'northeurope' and unitOfMeasure eq '1 Hour' and type eq 'Consumption' and isPrimaryMeterRegion eq true and currencyCode eq 'USD'",  # pylint: disable=line-too-long
            retries=42
        )
        self.assertEqual(skus[0].name, 'P4mv3')
        self.assertEqual(skus[0].region, 'northeurope')
        self.assertEqual(skus[0].price_by_hour, 1.6128)
        self.assertEqual(skus[0].description, 'Designed to provide enhanced performance for production apps and workload.')  # pylint: disable=line-too-long
        self.assertEqual(skus[0].cores, 16)
        self.assertEqual(skus[0].ram, 128)
        self.assertEqual(skus[0].disk, 250)

    def test_location(self):
        """
        Ensure location is properly updated.
        """
        sku.REQUEST = MagicMock()
        sku.REQUEST.return_value.json.return_value = self.skus

        sku.RETRY = MagicMock()
        sku.RETRY.return_value = 42

        skus = list(sku.get_skus('westeurope'))

        self.assertEqual(len(skus), 12)
        sku.REQUEST.assert_called_with(
            'GET',
            "https://prices.azure.com/api/retail/prices?$filter=serviceName eq 'Azure App Service' and contains(productName, 'Linux') and armRegionName eq 'westeurope' and unitOfMeasure eq '1 Hour' and type eq 'Consumption' and isPrimaryMeterRegion eq true and currencyCode eq 'USD'",  # pylint: disable=line-too-long
            retries=42
        )

    def test_raised(self):
        """
        Properly raise an exception when the API call has failed.
        """
        sku.REQUEST = MagicMock(side_effect=Exception('Bad request'))

        with self.assertRaises(InvalidSku):
            list(sku.get_skus('bad'))
