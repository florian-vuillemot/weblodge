import sys
import unittest

from weblodge.config import Config, ConfigField


config_fields = [
    ConfigField(
        name='app-name',
        description='The unique name of the application.',
        example='my-app'
    ),
    ConfigField(
        name='dest',
        description='Build destination.',
        example='my-dist',
        default='dist'
    ),
    ConfigField(
        name='src',
        description='Application location.',
        example='my-app/src',
        default='.'
    )
]

class TestConfig(unittest.TestCase):
    def test_default_values(self):
        sys.argv = [sys.argv[0], 'webapp', 'build']
        config = Config()
        self.assertEqual(config.target, 'webapp')
        self.assertEqual(config.action, 'build')

    def test_default(self):
        app_name = 'foo'
        sys.argv = [sys.argv[0], 'webapp', 'build', '--app-name', app_name]
        config = Config()

        config.load(config_fields)

        self.assertEqual(config['app_name'], app_name)
        self.assertEqual(config['dest'], config_fields[1].default)
        self.assertEqual(config['src'], config_fields[2].default)

    def test_override(self):
        src='my-src'
        dest='my-dist'
        app_name = 'foo'

        sys.argv = [sys.argv[0], 'webapp', 'build', '--app-name', app_name, '--dest', dest, '--src',  src]
        config = Config()

        config.load(config_fields)

        self.assertEqual(config['src'], src)
        self.assertEqual(config['dest'], dest)
        self.assertEqual(config['app_name'], app_name)

