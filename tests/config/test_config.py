import sys
import unittest

import weblodge.config as config


config_fields = [
    config.Field(
        name='app-name',
        description='The unique name of the application.',
    ),
    config.Field(
        name='dest',
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
        description='Application location.',
        attending_value=False,
    )
]

class TestConfig(unittest.TestCase):
    def test_default_values(self):
        sys.argv = [sys.argv[0], 'build']
        self.assertEqual(config.action(), 'build')

    def test_default(self):
        app_name = 'foo'
        sys.argv = [sys.argv[0], 'deploy', '--app-name', app_name]

        self.assertEqual(config.action(), 'deploy')

        _config = config.load(config_fields)
        self.assertEqual(_config['app_name'], app_name)
        self.assertEqual(_config['dest'], config_fields[1].default)
        self.assertEqual(_config['src'], config_fields[2].default)

    def test_override(self):
        src='my-src'
        dest='my-dist'
        app_name = 'foo'

        sys.argv = [sys.argv[0], 'build', '--app-name', app_name, '--dest', dest, '--src',  src]


        self.assertEqual(config.action(), 'build')
        
        _config = config.load(config_fields)
        self.assertEqual(_config['src'], src)
        self.assertEqual(_config['dest'], dest)
        self.assertEqual(_config['app_name'], app_name)

