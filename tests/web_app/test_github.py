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
        resource_group = MagicMock()
        azure_service.resource_groups.return_value = resource_group
        resource_group.exists.return_value = False

        config = GitHubConfig(
            subdomain='test-subdomain',
            branch='main-branch',
            username='test-username',
            repository='test-repository',
            location='northeurope'
        )

        github(azure_service, config)

        resource_group.create.assert_called_once_with('northeurope')
        azure_service.entra.github_application.assert_called_once_with(
            name='test-subdomain',
            branch='main-branch',
            username='test-username',
            repository='test-repository',
            resource_group=resource_group
        )

    def test_create_with_existing_resource_group(self):
        """
        Create an application.
        """
        azure_service = MagicMock()
        resource_group = MagicMock()
        azure_service.resource_groups.return_value = resource_group
        resource_group.exists.return_value = True

        config = GitHubConfig(
            subdomain='test-subdomain',
            branch='main-branch',
            username='test-username',
            repository='test-repository',
            location='northeurope'
        )

        github(azure_service, config)

        azure_service.entra.github_application.assert_called_once_with(
            name='test-subdomain',
            branch='main-branch',
            username='test-username',
            repository='test-repository',
            resource_group=resource_group
        )
