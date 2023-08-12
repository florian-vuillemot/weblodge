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

        workflow = github(azure_service, config)

        resource_group.create.assert_called_once_with('northeurope')
        azure_service.entra.github_application.assert_called_once_with(
            name='test-subdomain',
            branch='main-branch',
            username='test-username',
            repository='test-repository',
            resource_group=resource_group
        )
        self.assertEqual(workflow.branch, 'main-branch')
        self.assertIsNotNone(workflow.client_id)
        self.assertIsNotNone(workflow.subscription_id)
        self.assertIsNotNone(workflow.tenant_id)
        self.assertEqual(
            workflow.content,
            """\
# This file is generated by weblodge.
# Please do not edit it manually.
name: Weblodge deploy.
on:
  push:
    branches:
      - main-branch

permissions:
      id-token: write
      contents: read

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: 'Az CLI login'
        uses: azure/login@v1
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: 'Build and deploy.'
        run: |
          weblodge deploy --build
"""
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
            branch='main-branch-2',
            username='test-username',
            repository='test-repository',
            location='northeurope'
        )

        workflow = github(azure_service, config)

        azure_service.entra.github_application.assert_called_once_with(
            name='test-subdomain',
            branch='main-branch-2',
            username='test-username',
            repository='test-repository',
            resource_group=resource_group
        )
        self.assertEqual(workflow.branch, 'main-branch-2')
        self.assertIsNotNone(workflow.client_id)
        self.assertIsNotNone(workflow.subscription_id)
        self.assertIsNotNone(workflow.tenant_id)
        self.assertEqual(
            workflow.content,
            """\
# This file is generated by weblodge.
# Please do not edit it manually.
name: Weblodge deploy.
on:
  push:
    branches:
      - main-branch-2

permissions:
      id-token: write
      contents: read

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: 'Az CLI login'
        uses: azure/login@v1
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: 'Build and deploy.'
        run: |
          weblodge deploy --build
"""
        )
