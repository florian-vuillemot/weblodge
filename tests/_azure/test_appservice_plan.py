"""
App Service Plan Tests.
"""
import unittest

from weblodge._azure import AppService

from .cli import cli
from .mocks.app_services_plan import develop, staging, production, rg_develop, rg_staging


class TestAppService(unittest.TestCase):
    """
    App Service Plan CRUD Tests.
    """
    def setUp(self) -> None:
        self.app_service = AppService(cli)
        return super().setUp()

    def test_list(self):
        """
        Ensure the corresponding conversion is done by the list() method.
        """
        self.assertEqual(
            [develop, staging, production],
            self.app_service.list()
        )

    def test_get_without_rg(self):
        """
        Ensure the `get` method returns the first App Service Plan with the corresponding name
        when the Resource Group is not specified, i.e. here the first one.
        """
        asp = self.app_service.get(name='app-service', resource_group=rg_develop)
        self.assertEqual(develop, asp)

    def test_get_with_rg(self):
        """
        Ensure the `get` method returns the corresponding App Service Plan
        when the Resource Group is specified.
        """
        asp = self.app_service.get(name='app-service', resource_group=rg_staging)
        self.assertEqual(staging, asp)
