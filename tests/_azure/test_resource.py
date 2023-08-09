"""
Resource Group Tests.
"""
import json
from pathlib import Path
import unittest

from weblodge._azure.resource import Resource

from .cli import Cli


class MockResourceGroup(Resource):
    """
    OtherResourceGroup for test.
    """
    _cli_prefix = ''

    @property
    def id_(self) -> str:
        """
        Return the resource ID.
        """
        return self._from_az['id']

    def _load(self):
        """
        Load the second Resource Group data.
        """
        self._from_az.update(json.loads(
            Path('./tests/_azure/api_mocks/resource_groups.json').read_text(encoding='utf-8')
        )[1])
        return self


class TestResource(unittest.TestCase):
    """
    Resource tests.
    """
    def setUp(self) -> None:
        self.resources = json.loads(
            Path('./tests/_azure/api_mocks/resource_groups.json').read_text(encoding='utf-8')
        )
        return super().setUp()

    def test_standard_properties(self):
        """
        Test standard properties.
        """
        expected_output = self.resources[0]

        resource_group = MockResourceGroup(
            name=expected_output['name']
        )
        resource_group.set_cli(Cli(expected_output))

        self.assertEqual(resource_group.id_, expected_output['id'])
        self.assertEqual(resource_group.name, expected_output['name'])
        self.assertEqual(resource_group.tags, expected_output['tags'])

    def test_equality(self):
        """
        Test the create.
        """
        rg_foo = MockResourceGroup(name='foo')
        rg_bar = MockResourceGroup(name='bar')
        rg_foo_bis = MockResourceGroup(name='foo')

        self.assertEqual(rg_foo, rg_foo_bis)
        self.assertNotEqual(rg_foo, rg_bar)

    def test_all(self):
        """
        Test standard properties.
        """
        MockResourceGroup.set_cli(Cli([self.resources]))
        resources = list(MockResourceGroup.all())

        self.assertEqual(len(self.resources), len(resources))

        develop = self.resources[0]
        develop_resource_group = MockResourceGroup(
            name=develop['name'], from_az=develop
        )
        self.assertEqual(develop_resource_group, resources[0])
        self.assertEqual(develop_resource_group.id_, resources[0].id_)
        self.assertEqual(develop_resource_group.tags, resources[0].tags)
        self.assertEqual(develop_resource_group.name, resources[0].name)

        staging = self.resources[1]
        staging_resource_group = MockResourceGroup(
            name=staging['name'], from_az=staging
        )
        self.assertEqual(staging_resource_group, resources[1])
        self.assertEqual(staging_resource_group.id_, resources[1].id_)
        self.assertEqual(staging_resource_group.tags, resources[1].tags)
        self.assertEqual(staging_resource_group.name, resources[1].name)

        production = self.resources[2]
        production_resource_group = MockResourceGroup(
            name=production['name'], from_az=production
        )
        self.assertEqual(production_resource_group, resources[2])
        self.assertEqual(production_resource_group.id_, resources[2].id_)
        self.assertEqual(production_resource_group.tags, resources[2].tags)
        self.assertEqual(production_resource_group.name, resources[2].name)

    def test_exists(self):
        """
        Test exists.
        """
        MockResourceGroup.set_cli(Cli([self.resources]))

        staging = self.resources[1]
        staging_resource_group = MockResourceGroup(
            name=staging['name']
        )
        self.assertTrue(staging_resource_group.exists())
