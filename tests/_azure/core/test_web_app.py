import unittest

from u_deploy._azure import WebApp, WebAppHelper, ResourceGroup, ResourceGroupHelper
from u_deploy._azure.core.appservice import AppService

from .cli import cli


class TestWebApp(unittest.TestCase):
    develop = AppService(name='app-service', number_of_sites=2, sku='P1v3', resource_group=ResourceGroup(name='develop', location='northeurope'), location='North Europe')
    staging = AppService(name='app-service', number_of_sites=1, sku='P1v3', resource_group=ResourceGroup(name='staging', location='northeurope'), location='North Europe')
    production = AppService(name='app-service', number_of_sites=1, sku='P1v3', resource_group=ResourceGroup(name='production', location='northeurope'), location='North Europe')

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
                app_service=self.develop,
                resource_group=ResourceGroup(name="develop", location="northeurope"),
            ),
            WebApp(
                name="staging-app-service",
                host_names=["staging-app-service.azurewebsites.net"],
                kind="app,linux,container",
                location="North Europe",
                linux_fx_version="DOCKER|staging-registry.azurecr.io/app-service:main",
                app_service=self.staging,
                resource_group=ResourceGroup(name="staging", location="northeurope"),
            ),
            WebApp(
                name="production-app-service",
                host_names=["production-app-service.azurewebsites.net"],
                kind="app,linux,container",
                location="North Europe",
                linux_fx_version="DOCKER|production-registry.azurecr.io/app-service:main",
                app_service=self.production,
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
            app_service=self.staging,
            resource_group=ResourceGroup(name="staging", location="northeurope"),
        )

        r = self.web_app_helper.get(name)

        self.assertEqual(expected_output, r)
