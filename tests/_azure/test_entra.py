import json
import unittest
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

from weblodge._azure.entra import Entra

from .cli import Cli


class TestEntra(unittest.TestCase):
    def setUp(self) -> None:
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

    @patch("weblodge._azure.entra.tempfile.NamedTemporaryFile", new_callable=mock_open)
    def test_github_application(self, mock_tempfile):
        """
        Test the creation of a GitHub Application on Entra.
        """
        cli = Cli([self.account, self.entra_app, self.entra_sp, None, None])

        entra = Entra()
        entra.set_cli(cli)
        app = entra.github_application(
            name='app-name',
            branch='repo-branch',
            username='username',
            repository='repo-name',
            resource_group='app-name'
        )

        self.assertEqual(app.client_id, '29608a66-xxxx-xxxx-xxxxx-0ecee9437x42')
        self.assertEqual(app.tenant_id, '901536cd-xxxx-xxxx-xxxx-xxxxxxxxxxxx')
        self.assertEqual(app.subscription_id, '15be6804-xxxx-xxxx-xxxx-xxxxxxxxxxxx')
        mock_tempfile.assert_called_once_with(mode='w')
        mock_tempfile().write.assert_called_once_with(
            json.dumps(
                {
                    "name": 'weblodge-app-name',
                    "issuer": "https://token.actions.githubusercontent.com",
                    "subject": f"repo:username/repo-name:ref:repo-branch",
                    "description": f'WebLodge GitHub Application for application: weblodge-app-name',
                    "audiences": [
                        "api://AzureADTokenExchange"
                    ]
                }
            )
        )
