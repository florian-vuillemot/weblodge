import json
import unittest
from pathlib import Path

from u_deploy._azure.core.appservice import AppService, AppServiceHelper

from .cli import Cli


appservices_json = json.loads(Path('./tests/_azure/core/appservices_plan.json').read_text())

class TestAppService(unittest.TestCase):
    def setUp(self) -> None:
        self.cli = Cli()
        self.appservice_helper = AppServiceHelper(self.cli)
        self.cli.add_command('appservice plan list', appservices_json)
        return super().setUp()

    def test_list_appservice(self):
        expected_output = [
            AppService(name='app-service', number_of_sites=2, sku='P1v3', resource_group='develop', location='North Europe'),
            AppService(name='app-service', number_of_sites=1, sku='P1v3', resource_group='staging', location='North Europe'),
            AppService(name='app-service', number_of_sites=1, sku='P1v3', resource_group='production', location='North Europe'),
        ]

        r = self.appservice_helper.list()
        print(r)

        self.assertEqual(expected_output, r)

    def test_get_appservice(self):
        name = 'app-service'

        # Without resource_group
        resource_group = 'develop'
        expected_output = AppService(name=name, number_of_sites=2, sku='P1v3', resource_group=resource_group, location='North Europe')
        r = self.appservice_helper.get(name=name, resource_group=resource_group)
        self.assertEqual(expected_output, r)

        # With resource_group
        resource_group = 'staging'
        expected_output = AppService(name=name, number_of_sites=1, sku='P1v3', resource_group=resource_group, location='North Europe')
        r = self.appservice_helper.get(name=name, resource_group=resource_group)
        self.assertEqual(expected_output, r)
