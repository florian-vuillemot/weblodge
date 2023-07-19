"""
Resource Group Tests.
"""
import json
from pathlib import Path
import unittest

from weblodge._azure import ResourceGroup

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

        resource_group = ResourceGroup(name=expected_output['name'], cli=Cli(expected_output))

        self.assertEqual(resource_group.name, expected_output['name'])
        self.assertEqual(resource_group.location, expected_output['location'])
