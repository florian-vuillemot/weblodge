import unittest

from u_deploy._azure.core.resource_group import ResourceGroup, ResourceGroupHelper

from .cli import cli


class TestResourceGroup(unittest.TestCase):
    develop_resource_group = ResourceGroup(name='develop', location='northeurope')
    staging_resource_group = ResourceGroup(name='staging', location='northeurope')
    production_resource_group = ResourceGroup(name='production', location='northeurope')

    resource_groups = [
        develop_resource_group,
        staging_resource_group,
        production_resource_group,
    ]

    def setUp(self) -> None:
        self.resource_group_helper = ResourceGroupHelper(cli)

        return super().setUp()

    def test_list(self):
        r = self.resource_group_helper.list()
        self.assertEqual(self.resource_groups, r)

    def test_get(self):
        r = self.resource_group_helper.get(name=self.staging_resource_group.name)
        self.assertEqual(self.staging_resource_group, r)

    def test_create(self):
        r = self.resource_group_helper.create(
            name=self.staging_resource_group.name,
            location=self.staging_resource_group.location
        )
        self.assertEqual(self.staging_resource_group, r)
