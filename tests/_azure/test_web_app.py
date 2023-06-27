import unittest

from u_deploy._azure import WebApp

from .cli import cli
from .mocks.web_apps import develop, staging, production, rg_staging


class TestWebApp(unittest.TestCase):
    def setUp(self) -> None:
        self.web_app_helper = WebApp(cli)
        return super().setUp()

    def test_list(self):
        expected_output = [develop, staging, production]

        r = self.web_app_helper.list()
        self.assertEqual(expected_output, r)

    def test_get(self):
        name = 'staging-app-service'

        r = self.web_app_helper.get(name)
        self.assertEqual(staging, r)
