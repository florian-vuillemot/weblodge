import unittest

from u_deploy._azure import AppServiceHelper

from .cli import cli
from .mocks.app_services_plan import develop, staging, production, rg_develop, rg_staging


class TestAppService(unittest.TestCase):
    def setUp(self) -> None:
        self.appservice_helper = AppServiceHelper(cli)
        return super().setUp()

    def test_list(self):
        expected_output = [develop, staging, production]

        r = self.appservice_helper.list()
        self.assertEqual(expected_output, r)

    def test_get(self):
        name = 'app-service'

        # Without providing a ResourceGroup object.
        r = self.appservice_helper.get(name=name, resource_group=rg_develop)
        self.assertEqual(develop, r)

        # Providing a ResourceGroup object.
        r = self.appservice_helper.get(name=name, resource_group=rg_staging)
        self.assertEqual(staging, r)
