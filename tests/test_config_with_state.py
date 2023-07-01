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
        # Load the config from the state file.
        state_config = state.load(fd)

        # Get the config.
        _config = config.load(config_fields, state_config)
        self.assertEqual(_config, data)

    def test_load_update_dump(self):
        new_dist = 'new-dist'
        initial_config = {
            'app_name': 'my-src',
            'dist': 'my-dist',
            'src': 'foo'
        }
        new_config = {
            **initial_config,
            'dist': new_dist
        }
        fd = io.StringIO(json.dumps(initial_config))

        # Load the config from the disk.
        _config = state.load(fd)
        # Load the config from the CLI and override a value.
        sys.argv = [sys.argv[0], 'build', '--app-name', initial_config['app_name'], '--dist', new_dist]
        _config = config.load(config_fields, _config)

        # Save the config updated.
        fd.seek(0)
        state.dump(fd, _config)

        fd.seek(0)
        self.assertEqual(json.load(fd), new_config)
