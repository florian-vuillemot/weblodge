"""
Test the deploy fonction.
"""
import unittest
from unittest.mock import patch, MagicMock

from weblodge.web_app import NoMoreFreeApplicationAvailable
from weblodge.web_app.deploy import DeploymentConfig, deploy


class TestDeploy(unittest.TestCase):
    """
    Test state module.
    """
    @patch('weblodge._azure.WebApp')
    @patch('weblodge._azure.AppService')
    def no_more_free_app(self, webapp, app_services):
        """
        Ensure a cli exception is raised when no more free app is available.
        """
        webapp = MagicMock()
        webapp.return_value = None

        deployment_config = DeploymentConfig(
            subdomain='test',
            sku='F1',
            location='westeurope',
            environment='test',
            dist='dist',
            env_file='.env',
            log_level='info',
        )

        with self.assertRaises(NoMoreFreeApplicationAvailable):
            deploy(deployment_config)
