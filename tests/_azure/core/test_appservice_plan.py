import unittest

from u_deploy._azure import AppService, AppServiceHelper
from u_deploy._azure import ResourceGroup

from .cli import cli


class TestAppService(unittest.TestCase):
    def setUp(self) -> None:
        self.appservice_helper = AppServiceHelper(cli)
        return super().setUp()

    def test_list(self):
        expected_output = [
            AppService(name='app-service', number_of_sites=2, sku='P1v3', resource_group=ResourceGroup(name='develop', location='northeurope'), location='North Europe'),
            AppService(name='app-service', number_of_sites=1, sku='P1v3', resource_group=ResourceGroup(name='staging', location='northeurope'), location='North Europe'),
            AppService(name='app-service', number_of_sites=1, sku='P1v3', resource_group=ResourceGroup(name='production', location='northeurope'), location='North Europe'),
        ]

        r = self.appservice_helper.list()

        self.assertEqual(expected_output, r)

    def test_get(self):
        name = 'app-service'

        # Without providing a ResourceGroup object.
        resource_group = ResourceGroup(name='develop', location='northeurope')
        expected_output = AppService(name=name, number_of_sites=2, sku='P1v3', resource_group=resource_group, location='North Europe')
        r = self.appservice_helper.get(name=name, resource_group=resource_group)
        self.assertEqual(expected_output, r)

        # Providing a ResourceGroup object.
        resource_group = ResourceGroup(name='staging', location='northeurope')
        expected_output = AppService(name=name, number_of_sites=1, sku='P1v3', resource_group=resource_group, location='North Europe')
        r = self.appservice_helper.get(name=name, resource_group=resource_group)
        self.assertEqual(expected_output, r)
