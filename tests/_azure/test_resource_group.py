"""
Resource Group Tests.
"""
import json
from pathlib import Path
import unittest

from weblodge._azure.resource_group import ResourceGroup

from .cli import Cli


class TestResourceGroup(unittest.TestCase):
    """
    Resource Group tests.
    """
    def setUp(self) -> None:
        self.resource_groups = json.loads(
            Path('./tests/_azure/api_mocks/resource_groups.json').read_text(encoding='utf-8')
        )
        return super().setUp()

    def test_create(self):
        """
        Test the create.
        """
        expected_output = self.resource_groups[0]
        ResourceGroup.set_cli(Cli(expected_output))

        resource_group = ResourceGroup(
            name=expected_output['name'],
        )

        self.assertEqual(resource_group.name, expected_output['name'])
        self.assertEqual(resource_group.location, expected_output['location'])

    def test_all(self):
        """
        Test the all method.
        """
        ResourceGroup.set_cli(Cli([self.resource_groups]))

        resource_groups = ResourceGroup.all()
        self.assertEqual(len(list(resource_groups)), 3)
