"""
Web App Tests.
"""
import json
from pathlib import Path
import unittest
from unittest.mock import MagicMock

from weblodge._azure.web_app import WebApp, ResourceGroup, AppService, KeyVault

from .cli import Cli


class TestWebApp(unittest.TestCase):
    """
    Web App Tests.
    """
    def setUp(self) -> None:
        self.web_apps = json.loads(
            Path('./tests/_azure/api_mocks/web_apps.json').read_text(encoding='utf-8')
        )
        self.app_services = json.loads(
            Path('./tests/_azure/api_mocks/appservices_plan.json').read_text(encoding='utf-8')
        )
        self.resource_groups = json.loads(
            Path('./tests/_azure/api_mocks/resource_groups.json').read_text(encoding='utf-8')
        )
        return super().setUp()

    def test_create(self):
        """
        Create a Web App.
        """
        expected_output = self.web_apps[0]
        web_app = self._get_webapp()

        self.assertEqual(web_app.name, expected_output['name'])
        self.assertEqual(web_app.domain, expected_output['hostNames'][0])
        self.assertEqual(web_app.location, expected_output['location'])

    def test_update_environment(self):
        """
        Update Web App environment.
        """
        env = {'foo': 'bar', 'foo2': 'bar2'}
        kv_list = []
        kv_mock = MagicMock()
        kv_mock.set = lambda n, v: kv_list.append((n, v)) or MagicMock()

        cli = Cli(['set_env_foo', 'set_env_bar', 'invoke_app'])
        web_app = WebApp(
            name='webapp',
            resource_group=MagicMock(),
            app_service=MagicMock(),
            keyvault=kv_mock
        )
        web_app.set_cli(cli)

        web_app.update_environment(env)
        self.assertEqual(
            kv_list,
            [('foo', 'bar'), ('foo2', 'bar2')]
        )

    def test_deployment_in_progress(self):
        """
        Test the "deployment_in_progress" instance method.
        """
        deployments = json.loads(
            Path('./tests/_azure/api_mocks/web_app_log_deployment.json').read_text(encoding='utf-8')
        )
        web_app = self._get_webapp(cli=Cli([deployments]))

        self.assertTrue(web_app.deployment_in_progress())

    def _get_webapp(self, idx: int = 0, cli: Cli = None) -> WebApp:
        """
        Return a pre defined WebApp.
        """
        wp_data = self.web_apps[idx]

        resource_group = ResourceGroup(
            name=wp_data['resourceGroup'],
            from_az=self.resource_groups[idx]
        )
        asp = AppService(
            name=self.app_services[idx]['name'],
            resource_group=resource_group,
            from_az=self.app_services[idx]
        )
        keyvault = KeyVault(
            name=wp_data['name'],
            resource_group=resource_group
        )
        web_app = WebApp(
            name=wp_data['name'],
            resource_group=resource_group,
            app_service=asp,
            keyvault=keyvault
        )
        web_app.set_cli(cli or Cli(wp_data))

        return web_app
