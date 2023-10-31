"""
Test the deploy fonction.
"""
import os
import unittest
from unittest.mock import MagicMock

from weblodge.web_app import NoMoreFreeApplicationAvailable
from weblodge.web_app.deploy import DeploymentConfig, deploy


class TestDeploy(unittest.TestCase):
    """
    Test deploy function.
    """
    def test_web_app_exists(self):
        """
        Ensure no infrastructure is created if WebApp exists and correctly configured.
        """
        tier = 'F1'
        azure_service = self._default_asp()
        web_app = MagicMock()
        web_app.exists.return_value = True
        azure_service.get_web_app.return_value = web_app
        web_app.tier.name = tier
        web_app.tags = {'managedby': 'weblodge', 'environment': 'test'}

        log_level = MagicMock()
        azure_service.log_levels.return_value = log_level

        deployment_config = DeploymentConfig(
            subdomain='test',
            tier=tier,
            location='westeurope',
            environment='test',
            dist='dist',
            env_file='.donotexist',
            log_level='info',
        )
        deployment_config.env_update_waiting_time = 0

        deploy(azure_service, deployment_config)

        web_app.create.assert_not_called()
        web_app.deploy.assert_called_once_with(
            os.path.join(deployment_config.dist, deployment_config.package)
        )
        log_level.information.assert_called_once()
        web_app.update_environment.assert_not_called()

    def test_no_more_free_app(self):
        """
        Ensure a cli exception is raised when no more free app is available.
        """
        azure_service = self._default_asp()

        web_app = MagicMock()
        web_app.exists.return_value = False
        web_app.app_service.exists.return_value = False
        azure_service.web_apps.return_value = web_app

        deployment_config = DeploymentConfig(
            subdomain='test',
            tier='F1',
            location='westeurope',
            environment='test',
            dist='dist',
            env_file='.env',
            log_level='info',
        )

        with self.assertRaises(NoMoreFreeApplicationAvailable):
            deploy(azure_service, deployment_config)

    def _default_asp(self):
        """
        Return a AppServicePlan mock.
        """
        azure_service = MagicMock()
        azure_service.resource_groups = MagicMock()

        asp = MagicMock()
        asp.get_existing_free.return_value = MagicMock()
        azure_service.app_services = asp

        return azure_service
