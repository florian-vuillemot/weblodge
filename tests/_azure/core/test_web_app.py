import unittest

from u_deploy._azure import WebApp, WebAppHelper, ResourceGroup, ResourceGroupHelper

from .cli import cli


class TestWebApp(unittest.TestCase):
    def setUp(self) -> None:
        self.web_app_helper = WebAppHelper(cli)
        return super().setUp()

    def test_list(self):
        expected_output = [
            WebApp(
                name="develop-app-service",
                host_names=["develop-app-service.azurewebsites.net"],
                kind="app,linux,container",
                location="North Europe",
                linux_fx_version="DOCKER|develop-registry.azurecr.io/app-service:main",
                resource_group=ResourceGroup(name="develop", location="northeurope"),
            ),
            WebApp(
                name="staging-app-service",
                host_names=["staging-app-service.azurewebsites.net"],
                kind="app,linux,container",
                location="North Europe",
                linux_fx_version="DOCKER|staging-registry.azurecr.io/app-service:main",
                resource_group=ResourceGroup(name="staging", location="northeurope"),
            ),
            WebApp(
                name="production-app-service",
                host_names=["production-app-service.azurewebsites.net"],
                kind="app,linux,container",
                location="North Europe",
                linux_fx_version="DOCKER|production-registry.azurecr.io/app-service:main",
                resource_group=ResourceGroup(name="production", location="northeurope"),
            ),
        ]

        r = self.web_app_helper.list()

        self.assertEqual(expected_output, r)

    def test_get(self):
        name = 'staging-app-service'
        expected_output = WebApp(
            name=name,
            host_names=["staging-app-service.azurewebsites.net"],
            kind="app,linux,container",
            location="North Europe",
            linux_fx_version="DOCKER|staging-registry.azurecr.io/app-service:main",
            resource_group=ResourceGroup(name="staging", location="northeurope"),
        )

        r = self.web_app_helper.get(name)

        self.assertEqual(expected_output, r)
