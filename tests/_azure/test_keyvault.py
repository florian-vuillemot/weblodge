"""
KeyVault Tests.
"""
import json
from pathlib import Path
import unittest
from unittest.mock import MagicMock

from weblodge._azure.keyvault import KeyVault, KeyVaultSecret

from .cli import Cli


class TestKeyVault(unittest.TestCase):
    """
    KeyVault tests.
    """
    def setUp(self) -> None:
        self.keyvaults = json.loads(
            Path('./tests/_azure/api_mocks/keyvaults.json').read_text(encoding='utf-8')
        )
        self.keyvaults_secrets = json.loads(
            Path('./tests/_azure/api_mocks/keyvaults_secrets.json').read_text(encoding='utf-8')
        )
        self.keyvaults_show_secrets = json.loads(
            Path('./tests/_azure/api_mocks/keyvaults_show_secrets.json').read_text(encoding='utf-8')
        )
        return super().setUp()

    def test_create(self):
        """
        Test the create.
        """
        resource_group = MagicMock()
        resource_group.location = 'northeurope'
        resource_group.name = 'develop'
        resource_group.tags = {'managedby': 'weblodge'}
        expected_output = self.keyvaults[0]
        cli = Cli([expected_output, {'id': None}, None])

        keyvault = KeyVault(
            name=expected_output['name'],
            resource_group=resource_group
        )
        keyvault.set_cli(cli)

        keyvault.create()

        self.assertEqual(keyvault.tags, {'managedby': 'weblodge'})
        cli.asserts_commands_called([
            f'keyvault create --location {resource_group.location}'
        ])

    def test_get_secrets(self):
        """
        Test retrieving secrets values.
        """
        resource_group = MagicMock()
        expected_output = self.keyvaults_secrets[0]
        cli = Cli([
            expected_output,
            self.keyvaults_show_secrets[0][0],
            self.keyvaults_show_secrets[0][1],
        ])

        keyvault = KeyVault(
            name='develop_kv',
            resource_group=resource_group
        )
        keyvault.set_cli(cli)

        self.assertEqual(
            list(keyvault.get_all()),
            [
                KeyVaultSecret(
                    uri='https://develop_kv.vault.azure.net/secrets/foo/ee0d7259372a4ff69ec8c836e1cd7aec',
                    name='foo',
                    value='foo_value'
                ),
                KeyVaultSecret(
                    uri='https://develop_kv.vault.azure.net/secrets/bar/ee0d7259372a4ff69ec8c836e1cd7aec',
                    name='bar',
                    value='bar_value'
                )
            ]
        )
