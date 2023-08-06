"""
Parameters tests.

Ensure CLI parsing of parameters is done correctly.
"""
import sys
import unittest

from weblodge.config import Item as ConfigItem
from weblodge.parameters import Parser, ConfigIsDefined, ConfigIsNotDefined, ConfigTrigger


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
        ),
        ConfigItem(
            name='log_level',
            description='Log level.',
            default='info',
            values_allowed=['error', 'info', 'verbose', 'warning']
        ),
    ]

    def test_failed_when_missing_mandatory_item(self):
        """
        Ensure an error is raised when a mandatory item is missing from the CLI.
        """
        sys.argv = [sys.argv[0]]

        with self.assertRaises(SystemExit):
            Parser().load(self.config_fields)

    def test_default_values(self):
        """
        Ensure default values are loaded when no value are provided.
        """
        app_name = 'foo'
        sys.argv = [sys.argv[0], 'deploy', '--app-name', app_name]

        params = Parser().load(self.config_fields)

        self.assertEqual(params['app_name'], app_name)
        self.assertEqual(params['dist'], self.config_fields[1].default)
        self.assertEqual(params['src'], self.config_fields[2].default)
        self.assertEqual(params['log_level'], self.config_fields[4].default)

    def test_override(self):
        """
        Ensure parameters provided by the CLI replace the default values.
        """
        src = 'my-src'
        dist = 'my-dist'
        app_name = 'foo'
        log_level = 'verbose'

        sys.argv = [
            sys.argv[0], 'build',
            '--app-name', app_name,
            '--dist', dist,
            '--src',  src,
            '--log-level', log_level
        ]

        params = Parser().load(self.config_fields)
        self.assertEqual(params['src'], src)
        self.assertEqual(params['dist'], dist)
        self.assertEqual(params['app_name'], app_name)
        self.assertEqual(params['log_level'], log_level)

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
        params = Parser().load(self.config_fields)

        # Second set of parameters loaded that must override the first one.
        sys.argv = [sys.argv[0], 'build', '--dist', dist]
        params = Parser().load(override, params)

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

        params = Parser().load(self.config_fields, params)
        self.assertEqual(params['app_name'], app_name)
        self.assertEqual(params['src'], self.config_fields[2].default)
        self.assertEqual(params['dist'], self.config_fields[1].default)

    def test_trigger_is_defined(self):
        """
        Ensure trigger is call when defined.
        """
        def _must_be_called(_config):
            self.assertNotIn('yes', _config)
            return {
                **_config,
                'called': True
            }

        def _must_not_be_called(_config):
            self.assertRaises('Must not be called.')

        yes_trigger = ConfigIsDefined(
            name='yes',
            description='Do not prompt validation.',
            trigger=_must_be_called,
            attending_value=False
        )
        no_trigger = ConfigIsDefined(
            name='no',
            description='Do not prompt validation.',
            trigger=_must_not_be_called,
            attending_value=False
        )

        # First set of parameters loaded.
        # `dist` is loaded as a default value.
        sys.argv = [sys.argv[0], 'build', '--yes', '--app-name', 'foo']
        parser = Parser()
        parser.trigger_once(yes_trigger)
        parser.trigger_once(no_trigger)
        config = parser.load(self.config_fields)

        # Ensure the trigger was called.
        self.assertIn('called', config)
        # Ensure the config is not polluted by triggers.
        self.assertNotIn('yes', config)
        self.assertNotIn('no', config)

    def test_trigger_is_not_defined(self):
        """
        Ensure trigger is call when not defined.
        """
        def _must_be_called(_config):
            self.assertNotIn('yes', _config)
            return {
                **_config,
                'called': True
            }

        def _must_not_be_called(_config):
            self.assertRaises('Must not be called.')

        yes_trigger = ConfigIsNotDefined(
            name='yes',
            description='Do not prompt validation.',
            trigger=_must_be_called,
            attending_value=False
        )
        no_trigger = ConfigIsNotDefined(
            name='no',
            description='Do not prompt validation.',
            trigger=_must_not_be_called,
            attending_value=False
        )

        # First set of parameters loaded.
        # `dist` is loaded as a default value.
        sys.argv = [sys.argv[0], 'build', '--no', '--app-name', 'foo']
        parser = Parser()
        parser.trigger_once(yes_trigger)
        parser.trigger_once(no_trigger)
        config = parser.load(self.config_fields)

        # Ensure the trigger was called.
        self.assertIn('called', config)
        # Ensure the config is not polluted by triggers.
        self.assertNotIn('yes', config)
        self.assertNotIn('no', config)

    def test_trigger_everytime(self):
        """
        Ensure trigger is call if defined or not.
        """
        def _defined(_config):
            self.assertNotIn('yes', _config)
            return {
                **_config,
                'defined_called': True
            }
        def _not_defined(_config):
            self.assertNotIn('no', _config)
            return {
                **_config,
                'not_defined_called': True
            }

        defined_trigger = ConfigTrigger(
            name='yes',
            description='Validation.',
            trigger=_defined,
            attending_value=False
        )
        not_defined_trigger = ConfigTrigger(
            name='no',
            description='No validation.',
            trigger=_not_defined,
            attending_value=False
        )

        # First set of parameters loaded.
        # `dist` is loaded as a default value.
        sys.argv = [sys.argv[0], 'build', '--yes', '--app-name', 'foo']
        parser = Parser()
        parser.trigger_once(defined_trigger)
        parser.trigger_once(not_defined_trigger)
        config = parser.load(self.config_fields)

        # Ensure the trigger was called.
        self.assertIn('defined_called', config)
        self.assertIn('not_defined_called', config)

    def test_allowed_values(self):
        """
        Ensure only allowed values are accepted.
        """
        log_level = 'not-allowed'

        sys.argv = [sys.argv[0], 'build', '--log-level', log_level]

        with self.assertRaises(SystemExit):
            Parser().load(self.config_fields)
