"""
Resource Group Tests.
"""
import unittest

from weblodge._azure import ResourceGroup

from .cli import cli
from .mocks.resource_group import develop, staging, production


class TestResourceGroup(unittest.TestCase):
    """
    Resource Group CRUD Tests.
    """
    def setUp(self) -> None:
        self.resource_group = ResourceGroup(cli)

        return super().setUp()

    def test_list(self):
        """
        Ensure the corresponding conversion is done by the `list` method.
        """
        self.assertEqual(
            [develop, staging, production],
            self.resource_group.list()
        )

    def test_get(self):
        """
        Ensure the `get` method returns the corresponding Resource Group.
        """
        self.assertEqual(
            staging,
            self.resource_group.get(name=staging.name)
        )

    def test_create(self):
        """
        Ensure the `create` method returns the corresponding Resource Group.
        """
        self.assertEqual(
            staging,
            self.resource_group.create(
                name=staging.name,
                location=staging.location
            )
        )
