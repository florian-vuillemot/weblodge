import json
import unittest
from pathlib import Path

from u_deploy._azure import WebApp, WebAppHelper

from .cli import Cli


web_apps_json = json.loads(Path('./tests/_azure/core/web_apps.json').read_text())

class TestWebApp(unittest.TestCase):
    def setUp(self) -> None:
        self.cli = Cli()
        self.web_app_helper = WebAppHelper(self.cli)
        self.cli.add_command('webapp list', web_apps_json)
        return super().setUp()

    def test_list_web_app(self):
        expected_output = [
            WebApp(
                name="develop-app-service",
                resource_group="develop",
                host_names=["develop-app-service.azurewebsites.net"],
                kind="app,linux,container",
                location="North Europe",
                linux_fx_version="DOCKER|develop-registry.azurecr.io/app-service:main"
            ),
            WebApp(
                name="staging-app-service",
                resource_group="staging",
                host_names=["staging-app-service.azurewebsites.net"],
                kind="app,linux,container",
                location="North Europe",
                linux_fx_version="DOCKER|staging-registry.azurecr.io/app-service:main"
            ),
            WebApp(
                name="production-app-service",
                resource_group="production",
                host_names=["production-app-service.azurewebsites.net"],
                kind="app,linux,container",
                location="North Europe",
                linux_fx_version="DOCKER|production-registry.azurecr.io/app-service:main"
            ),
        ]

        r = self.web_app_helper.list()

        self.assertEqual(expected_output, r)

    def test_get_web_app(self):
        name = 'staging-app-service'
        expected_output = WebApp(
            name=name,
            resource_group="staging",
            host_names=["staging-app-service.azurewebsites.net"],
            kind="app,linux,container",
            location="North Europe",
            linux_fx_version="DOCKER|staging-registry.azurecr.io/app-service:main"
        )

        r = self.web_app_helper.get(name)

        self.assertEqual(expected_output, r)
