"""
Web App Tests.
"""
import unittest

from weblodge._azure import WebApp

from .cli import cli
from .mocks.web_apps import develop, staging, production


class TestWebApp(unittest.TestCase):
    """
    Web App CRUD Tests.
    """
    def setUp(self) -> None:
        self.web_app_helper = WebApp(cli)
        return super().setUp()

    def test_list(self):
        """
        Ensure the corresponding conversion is done by the `list` method.
        """
        self.assertEqual(
            [develop, staging, production],
            self.web_app_helper.list()
        )

    def test_get(self):
        """
        Ensure the `get` method returns the corresponding Web App.
        """
        self.assertEqual(
            staging,
            self.web_app_helper.get('staging-app-service')
        )
