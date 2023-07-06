"""
Parameters tests.

Ensure CLI parsing of parameters is done correctly.
"""
import sys
import unittest

import weblodge.parameters as parameters
from weblodge.config import Item as ConfigItem


class TestGlobalParameters(unittest.TestCase):
    """
    Test global parameters parsing.
    """
    def test_action(self):
        """
        The action parameter is required and must be parsed.
        """
        sys.argv = [sys.argv[0], 'build']

        self.assertEqual(parameters.weblodge().action, 'build')

    def test_failed_when_action_is_missing(self):
        """
        The action parameter is required, if not provided, error must be returned.
        """
        sys.argv = [sys.argv[0]]

        with self.assertRaises(SystemExit):
            parameters.weblodge()

    def test_config_file(self):
        """
        The config file can be provided.
        """
        filename = 'my-config-file'

        sys.argv = [sys.argv[0], 'deploy', '--config-file', filename]

        self.assertEqual(parameters.weblodge().action, 'deploy')
        self.assertEqual(parameters.weblodge().config_filename, filename)


class TestConfigBasedParameters(unittest.TestCase):
    """
    Test config based parameters parsing.
    Those parameters are loaded from dynamics configuration provided by modules.
    """
    config_fields = [
        ConfigItem(
            name='app_name',
            description='The unique name of the application.',
        ),
        ConfigItem(
            name='dist',
            description='Build destination.',
            default='dist'
        ),
        ConfigItem(
            name='src',
            description='Application location.',
            default='.'
        ),
        ConfigItem(
            name='build',
            description='Application must be build before.',
            attending_value=False,
        )
    ]

    def test_failed_when_missing_mandatory_item(self):
        """
        Ensure an error is raised when a mandatory item is missing from the CLI.
        """
        sys.argv = [sys.argv[0]]

        with self.assertRaises(SystemExit):
            parameters.load(self.config_fields)

    def test_default_values(self):
        """
        Ensure default values are loaded when no value are provided.
        """
        app_name = 'foo'
        sys.argv = [sys.argv[0], 'deploy', '--app-name', app_name]

        params = parameters.load(self.config_fields)

        self.assertEqual(params['app_name'], app_name)
        self.assertEqual(params['dist'], self.config_fields[1].default)
        self.assertEqual(params['src'], self.config_fields[2].default)

    def test_override(self):
        """
        Ensure parameters provided by the CLI replace the default values.
        """
        src='my-src'
        dist='my-dist'
        app_name = 'foo'

        sys.argv = [sys.argv[0], 'build', '--app-name', app_name, '--dist', dist, '--src',  src]

        params = parameters.load(self.config_fields)
        self.assertEqual(params['src'], src)
        self.assertEqual(params['dist'], dist)
        self.assertEqual(params['app_name'], app_name)

    def test_override_existing_parameters(self):
        """
        Parameters can be load based on a previous set of parameters.
        The latest loaded parameters override the previous ones.
        """
        dist='my-real-dist'
        app_name = 'foo'

        override = [
            ConfigItem(
                name='dist',
                description='Build destination.',
                default='default-will-be-ignored'
            )
        ]

        # First set of parameters loaded.
        # `dist` is loaded as a default value.
        sys.argv = [sys.argv[0], 'build', '--app-name', app_name]
        params = parameters.load(self.config_fields)

        # Second set of parameters loaded that must override the first one.
        sys.argv = [sys.argv[0], 'build', '--dist', dist]
        params = parameters.load(override, params)

        self.assertEqual(params['dist'], dist)
        self.assertEqual(params['app_name'], app_name)
        self.assertEqual(params['src'], self.config_fields[2].default)

    def test_no_require_when_override(self):
        """
        If a parameter was already loaded, it is not required to be provided again.
        """
        app_name = 'foo'

        params = {
            'app_name': app_name
        }

        sys.argv = [sys.argv[0], 'build']

        params = parameters.load(self.config_fields, params)
        self.assertEqual(params['app_name'], app_name)
        self.assertEqual(params['src'], self.config_fields[2].default)
        self.assertEqual(params['dist'], self.config_fields[1].default)
