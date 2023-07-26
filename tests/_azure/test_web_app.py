"""
Web App Tests.
"""
import json
from pathlib import Path
import unittest

from weblodge._azure import WebApp, ResourceGroup, AppService

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
            cli=None,
            from_az=self.resource_groups[idx]
        )
        asp = AppService(
            name=self.app_services[idx]['name'],
            resource_group=resource_group,
            cli=None,
            from_az=self.app_services[idx]
        )
        web_app = WebApp(
            name=wp_data['name'],
            resource_group=resource_group,
            app_service=asp,
            cli=cli if cli else Cli(wp_data)
        )

        return web_app
