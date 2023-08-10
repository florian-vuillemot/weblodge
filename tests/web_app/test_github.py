"""
Test the GitHub command.
"""
import unittest
from unittest.mock import MagicMock

from weblodge.web_app.github import GitHubConfig, github


class TestGitHub(unittest.TestCase):
    """
    Test the GitHub command.
    """
    def test_create(self):
        """
        Create an application.
        """
        azure_service = MagicMock()

        config = GitHubConfig(
            subdomain='test-subdomain',
            branch='main-branch',
            username='test-username',
            repository='test-repository',
        )

        github(azure_service, config)

        azure_service.entra.github_application.assert_called_once_with(
            name='test-subdomain',
            branch='main-branch',
            username='test-username',
            repository='test-repository',
            resource_group='test-subdomain'
        )
