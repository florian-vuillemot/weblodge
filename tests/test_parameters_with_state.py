"""
Ensure the integration between parameters and state works as expected.
"""
import io
import json
import sys
import unittest

import weblodge.state as state
from weblodge.parameters import Parser
from weblodge.config import Item as ConfigItem


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
    )
]


class TestParametersWithState(unittest.TestCase):
    """
    Ensure the integration between parameters and state works as expected.

    Both module will be used together without knowing each other, those tests
    ensure the integration works as expected.
    """
    def test_dump(self):
        """
        Ensure parameters can be loaded from the CLI then dumped to the state file.
        """
        src = 'my-src'
        dist = 'my-dist'
        app_name = 'foo'
        file = io.StringIO()

        sys.argv = [sys.argv[0], 'build', '--app-name', app_name, '--dist', dist, '--src',  src]

        # Create the config as if it was loaded from the command line.
        params = Parser().load(config_fields)
        # Save the config to the file descriptor.
        state.dump(file, params)

        file.seek(0)
        self.assertEqual(
            json.load(file),
            {
                'app_name': app_name,
                'dist': dist,
                'src': src
            }
        )

    def test_load(self):
        """
        Ensure parameters can be loaded from the state and merged with CLI parameters.
        """
        data = {
            'app_name': 'my-src',
            'dist': 'my-dist',
            'src': 'foo'
        }
        file = io.StringIO(json.dumps(data))

        # Load the config from the state file.
        state_config = state.load(file)

        # Load the config from the CLI without args.
        sys.argv = [sys.argv[0], 'build', '--app-name', data['app_name']]

        # Merge configs.
        params = Parser().load(config_fields, state_config)
        self.assertEqual(params, data)

    def test_load_update_dump(self):
        """
        Run a full cycle of load, update and dump.
        """
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
        file = io.StringIO(json.dumps(initial_config))

        # Load the config from the disk.
        params = state.load(file)
        # Load the config from the CLI and override a value.
        sys.argv = [sys.argv[0], 'build', '--app-name', initial_config['app_name'], '--dist', new_dist]
        params = Parser().load(config_fields, params)

        # Save the config updated.
        file.seek(0)
        state.dump(file, params)

        file.seek(0)
        self.assertEqual(json.load(file), new_config)
