"""
Test the all fonction.
"""
import unittest
from unittest.mock import MagicMock

from weblodge.web_app._all import _all


class TestAll(unittest.TestCase):
    """
    Test all function module.
    """
    def test_multiple_web_app(self):
        """
        Retrieve multiple WebApp.
        """
        azure_service = MagicMock()
        azure_service.resource_groups.all.return_value = [
            MagicMock(tags={'contains': 'webapp'}),
            MagicMock(tags={'contains': 'other'}),
            MagicMock(tags={'contains': 'webapp'}),
        ]

        rgs = _all(azure_service)

        self.assertEqual(len(list(rgs)), 2)

    def test_no_web_app(self):
        """
        No WebApp.
        """
        azure_service = MagicMock()
        azure_service.resource_groups.all.return_value = []

        rgs = _all(azure_service)

        self.assertEqual(len(list(rgs)), 0)

    def test_no_correct_app(self):
        """
        No correct WebApp to return.
        """
        azure_service = MagicMock()
        azure_service.resource_groups.all.return_value = [
            MagicMock(tags={'contains': 'other'}),
        ]

        rgs = _all(azure_service)

        self.assertEqual(len(list(rgs)), 0)
