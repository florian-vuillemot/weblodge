import io
import json
import sys
import unittest

import weblodge.state as state
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
    )
]

class TestConfigWithState(unittest.TestCase):
    def test_dump(self):
        src = 'my-src'
        dist = 'my-dist'
        app_name = 'foo'
        fd = io.StringIO()

        sys.argv = [sys.argv[0], 'build', '--app-name', app_name, '--dist', dist, '--src',  src]

        # Create the config as if it was loaded from the command line.
        _config = config.load(config_fields)
        # Save the config to the file descriptor.
        state.dump(fd, _config)

        fd.seek(0)
        self.assertEqual(
            json.load(fd),
            {
                'app_name': app_name,
                'dist': dist,
                'src': src
            }
        )

    def test_load(self):
        data = {
            'app_name': 'my-src',
            'dist': 'my-dist',
            'src': 'foo'
        }
        fd = io.StringIO(json.dumps(data))

        # Load the config from the CLI without args.
        sys.argv = [sys.argv[0], 'build', '--app-name', data['app_name']]
        cli_config = config.load(config_fields)
        # Load the config from the state file.
        state_config = state.load(fd)

        # Merge the two configs.
        _config = {**cli_config, **state_config}

        self.assertEqual(_config, data)
