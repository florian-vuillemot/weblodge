import sys
import unittest

import weblodge.parameters as parameters
from weblodge.config import Item as ConfigItem


config_fields = [
    ConfigItem(
        name='app-name',
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

class TestConfig(unittest.TestCase):
    def test_default_values(self):
        sys.argv = [sys.argv[0], 'build']

        self.assertEqual(parameters.weblodge().action, 'build')

    def test_config_file(self):
        filename = 'my-config-file'

        sys.argv = [sys.argv[0], 'deploy', '--config-file', filename]

        self.assertEqual(parameters.weblodge().action, 'deploy')
        self.assertEqual(parameters.weblodge().config_filename, filename)

    def test_default(self):
        app_name = 'foo'
        sys.argv = [sys.argv[0], 'deploy', '--app-name', app_name]

        _config = parameters.load(config_fields)
        self.assertEqual(_config['app_name'], app_name)
        self.assertEqual(_config['dist'], config_fields[1].default)
        self.assertEqual(_config['src'], config_fields[2].default)

    def test_override(self):
        src='my-src'
        dist='my-dist'
        app_name = 'foo'

        sys.argv = [sys.argv[0], 'build', '--app-name', app_name, '--dist', dist, '--src',  src]
        
        _config = parameters.load(config_fields)
        self.assertEqual(_config['src'], src)
        self.assertEqual(_config['dist'], dist)
        self.assertEqual(_config['app_name'], app_name)

    def test_override(self):
        """
        Test the override of passed config.
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

        sys.argv = [sys.argv[0], 'build', '--app-name', app_name]

        _config = parameters.load(config_fields)
        
        sys.argv = [sys.argv[0], 'build', '--dist', dist]
        _config = parameters.load(override, _config)

        self.assertEqual(_config['dist'], dist)
        self.assertEqual(_config['app_name'], app_name)
        self.assertEqual(_config['src'], config_fields[2].default)


    def test_no_override(self):
        """
        Ensure previous set values are not overriden by a default.
        """
        dist='no-override'
        app_name = 'foo'

        no_override = [
            ConfigItem(
                name='dist',
                description='Build destination.',
                default=dist
            )
        ]

        sys.argv = [sys.argv[0], 'build', '--app-name', app_name]

        _config = parameters.load(config_fields)
        # Value not defined in args, so it should be the default value.
        _config = parameters.load(no_override, _config)

        self.assertEqual(_config['app_name'], app_name)
        self.assertEqual(_config['src'], config_fields[2].default)
        self.assertEqual(_config['dist'], config_fields[1].default)
