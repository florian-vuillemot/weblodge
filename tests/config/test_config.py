import sys
import unittest

import weblodge.config as config


config_fields = [
    config.Field(
        name='app-name',
        description='The unique name of the application.',
    ),
    config.Field(
        name='dist',
        description='Build destination.',
        default='dist'
    ),
    config.Field(
        name='src',
        description='Application location.',
        default='.'
    ),
    config.Field(
        name='build',
        description='Application must be build before.',
        attending_value=False,
    )
]

class TestConfig(unittest.TestCase):
    def test_default_values(self):
        sys.argv = [sys.argv[0], 'build']

        self.assertEqual(config.weblodge().action, 'build')

    def test_config_file(self):
        filename = 'my-config-file'

        sys.argv = [sys.argv[0], 'deploy', '--config-file', filename]

        self.assertEqual(config.weblodge().action, 'deploy')
        self.assertEqual(config.weblodge().config_filename, filename)

    def test_default(self):
        app_name = 'foo'
        sys.argv = [sys.argv[0], 'deploy', '--app-name', app_name]

        _config = config.load(config_fields)
        self.assertEqual(_config['app_name'], app_name)
        self.assertEqual(_config['dist'], config_fields[1].default)
        self.assertEqual(_config['src'], config_fields[2].default)

    def test_override(self):
        src='my-src'
        dist='my-dist'
        app_name = 'foo'

        sys.argv = [sys.argv[0], 'build', '--app-name', app_name, '--dist', dist, '--src',  src]
        
        _config = config.load(config_fields)
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
            config.Field(
                name='dist',
                description='Build destination.',
                default='default-will-be-ignored'
            )
        ]

        sys.argv = [sys.argv[0], 'build', '--app-name', app_name]

        _config = config.load(config_fields)
        
        sys.argv = [sys.argv[0], 'build', '--dist', dist]
        _config = config.load(override, _config)

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
            config.Field(
                name='dist',
                description='Build destination.',
                default=dist
            )
        ]

        sys.argv = [sys.argv[0], 'build', '--app-name', app_name]

        _config = config.load(config_fields)
        # Value not defined in args, so it should be the default value.
        _config = config.load(no_override, _config)

        self.assertEqual(_config['app_name'], app_name)
        self.assertEqual(_config['src'], config_fields[2].default)
        self.assertEqual(_config['dist'], config_fields[1].default)
