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
        self.app_service = json.loads(
            Path('./tests/_azure/api_mocks/appservices_plan.json').read_text(encoding='utf-8')
        )
        self.resource_group = json.loads(
            Path('./tests/_azure/api_mocks/resource_groups.json').read_text(encoding='utf-8')
        )[0]
        return super().setUp()

    def test_create(self):
        """
        Create a Web App.
        """
        expected_output = self.web_apps[0]

        resource_group = ResourceGroup(
            name=expected_output['resourceGroup'],
            cli=None,
            from_az=self.resource_group
        )
        asp = AppService(
            name=self.app_service[0]['name'],
            resource_group=resource_group,
            cli=None,
            from_az=self.app_service[0]
        )

        web_app = WebApp(
            name=expected_output['name'],
            resource_group=resource_group,
            app_service=asp,
            cli=Cli(expected_output)
        )

        self.assertEqual(web_app.name, expected_output['name'])
        self.assertEqual(web_app.domain, expected_output['hostNames'][0])
        self.assertEqual(web_app.location, expected_output['location'])
