import unittest

from u_deploy._azure.core.resource_group import ResourceGroup, ResourceGroupHelper

from .cli import cli
from .mocks.resource_group import develop, staging, production


class TestResourceGroup(unittest.TestCase):
    resource_groups = [develop, staging, production]

    def setUp(self) -> None:
        self.resource_group_helper = ResourceGroupHelper(cli)

        return super().setUp()

    def test_list(self):
        r = self.resource_group_helper.list()
        self.assertEqual(self.resource_groups, r)

    def test_get(self):
        r = self.resource_group_helper.get(name=staging.name)
        self.assertEqual(staging, r)

    def test_create(self):
        r = self.resource_group_helper.create(
            name=staging.name,
            location=staging.location
        )
        self.assertEqual(staging, r)
