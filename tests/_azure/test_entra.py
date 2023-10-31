"""
Test the Entra facade.
"""
import json
import unittest
from pathlib import Path
from unittest.mock import mock_open, patch

from weblodge._azure.entra import Entra
from weblodge._azure.resource_group import ResourceGroup

from .cli import Cli


class TestEntra(unittest.TestCase):
    """
    Test the Entra facade.
    """
    def setUp(self) -> None:
        self.resource_groups = json.loads(
            Path('./tests/_azure/api_mocks/resource_groups.json').read_text(encoding='utf-8')
        )
        self.account = json.loads(
            Path('./tests/_azure/api_mocks/account_show.json').read_text(encoding='utf-8')
        )
        self.entra_app = json.loads(
            Path('./tests/_azure/api_mocks/entra_app.json').read_text(encoding='utf-8')
        )
        self.entra_sp = json.loads(
            Path('./tests/_azure/api_mocks/entra_sp.json').read_text(encoding='utf-8')
        )
        return super().setUp()

    @patch("weblodge._azure.entra.os")
    @patch("weblodge._azure.entra.json.dump")
    @patch("weblodge._azure.entra.tempfile.NamedTemporaryFile", new_callable=mock_open)
    def test_github_application(self, mock_tempfile, mock_dump, mock_os):
        """
        Test the creation of a GitHub Application on Entra with an existing Resource Group.
        """
        cli = Cli([self.resource_groups, self.account, [], self.entra_app, [], self.entra_sp, [], None, [], None])

        Entra.set_cli(cli)
        ResourceGroup.set_cli(cli)

        app = Entra.get_github_application(
            subdomain='develop',
            branch='repo-branch',
            username='username',
            repository='repo-name',
            location='northeurope',
        )

        # Ensure App and SP were created.
        cli.asserts_commands_called(('ad app create', 'ad sp create'))

        self.assertEqual(app.client_id, '29608a66-xxxx-xxxx-xxxxx-0ecee9437x42')
        self.assertEqual(app.tenant_id, '901536cd-xxxx-xxxx-xxxx-xxxxxxxxxxxx')
        self.assertEqual(app.subscription_id, '15be6804-xxxx-xxxx-xxxx-xxxxxxxxxxxx')
        mock_dump.assert_called_once_with(
            {
                "name": 'weblodge-develop',
                "issuer": "https://token.actions.githubusercontent.com",
                "subject": "repo:username/repo-name:ref:refs/heads/repo-branch",
                "description": 'WebLodge GitHub Application for application: weblodge-develop',
                "audiences": [
                    "api://AzureADTokenExchange"
                ]
            },
            mock_tempfile()
        )
        mock_os.unlink.assert_called()

    @patch("weblodge._azure.entra.os")
    @patch("weblodge._azure.entra.json.dump")
    @patch("weblodge._azure.entra.tempfile.NamedTemporaryFile", new_callable=mock_open)
    def test_github_application_and_sp_already_exists(self, mock_tempfile, mock_dump, mock_os):
        """
        Test the creation of a GitHub Application on Entra.
        """
        cli = Cli([self.resource_groups, self.account, [self.entra_app], [self.entra_sp], [], None, [], None])

        Entra.set_cli(cli)
        ResourceGroup.set_cli(cli)

        app = Entra.get_github_application(
            subdomain='develop',
            branch='repo-branch',
            username='username',
            repository='repo-name',
            location='northeurope',
        )

        # Ensure App and SP were not created.
        cli.asserts_commands_not_called(('ad app create', 'ad sp create'))

        self.assertEqual(app.client_id, '29608a66-xxxx-xxxx-xxxxx-0ecee9437x42')
        self.assertEqual(app.tenant_id, '901536cd-xxxx-xxxx-xxxx-xxxxxxxxxxxx')
        self.assertEqual(app.subscription_id, '15be6804-xxxx-xxxx-xxxx-xxxxxxxxxxxx')
        mock_dump.assert_called_once_with(
            {
                "name": 'weblodge-develop',
                "issuer": "https://token.actions.githubusercontent.com",
                "subject": "repo:username/repo-name:ref:refs/heads/repo-branch",
                "description": 'WebLodge GitHub Application for application: weblodge-develop',
                "audiences": [
                    "api://AzureADTokenExchange"
                ]
            },
            mock_tempfile()
        )
        mock_os.unlink.assert_called()

    @patch("weblodge._azure.entra.os.unlink")
    @patch("weblodge._azure.entra.tempfile.NamedTemporaryFile", new_callable=mock_open)
    def test_github_credential_already_exists(self, mock_tempfile, mock_unlink):
        """
        Test the creation of a GitHub Application on Entra.
        """
        github_federated_cred_specs = {
            "issuer": "https://token.actions.githubusercontent.com",
            "subject": "repo:username/repo-name:ref:refs/heads/repo-branch",
            "audiences": [
                "api://AzureADTokenExchange"
            ]
        }
        cli = Cli([
            self.resource_groups, self.account, [self.entra_app], [self.entra_sp], [1], [github_federated_cred_specs]
        ])

        Entra.set_cli(cli)
        ResourceGroup.set_cli(cli)

        app = Entra.get_github_application(
            subdomain='develop',
            branch='repo-branch',
            username='username',
            repository='repo-name',
            location='northeurope',
        )

        # Ensure App and SP were not created.
        cli.asserts_commands_not_called((
            'ad app create', 'ad sp create',
            'ad app create', 'role assignment create'
        ))

        self.assertEqual(app.client_id, '29608a66-xxxx-xxxx-xxxxx-0ecee9437x42')
        self.assertEqual(app.tenant_id, '901536cd-xxxx-xxxx-xxxx-xxxxxxxxxxxx')
        self.assertEqual(app.subscription_id, '15be6804-xxxx-xxxx-xxxx-xxxxxxxxxxxx')
        mock_unlink.assert_not_called()
        mock_tempfile.assert_not_called()
