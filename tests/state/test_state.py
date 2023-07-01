import sys
import unittest

import weblodge.config as config
import weblodge.state as state


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
        description='Application must be build before.',
        attending_value=False,
    )
]

class TestState(unittest.TestCase):
    def test_state(self):
        _config = config.load(config_fields)

