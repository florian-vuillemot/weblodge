import json
import unittest
from pathlib import Path

from u_deploy._azure.core.resource_group import ResourceGroup, ResourceGroupHelper

from .cli import Cli


resource_groups_json = json.loads(Path('./tests/_azure/core/resource_groups.json').read_text())

class TestResourceGroup(unittest.TestCase):
    def setUp(self) -> None:
        self.cli = Cli()

        self.resource_group_helper = ResourceGroupHelper(self.cli)
        self.cli.add_command('group list', resource_groups_json)

        return super().setUp()

    def test_list_resource_group(self):
        expected_output = [
            ResourceGroup(name='develop', location='northeurope'),
            ResourceGroup(name='staging', location='northeurope'),
            ResourceGroup(name='production', location='northeurope'),
        ]

        r = self.resource_group_helper.list()

        self.assertEqual(expected_output, r)

    def test_get_resource_group(self):
        name = 'staging'

        expected_output = ResourceGroup(name=name, location='northeurope')
        r = self.resource_group_helper.get(name=name)
        self.assertEqual(expected_output, r)
