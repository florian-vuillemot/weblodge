"""
Test state module.
"""
import io
import json
import unittest

import weblodge.state as state


class TestState(unittest.TestCase):
    """
    Test state module.
    """
    def test_dump(self):
        """
        Test the dump function.
        """
        config = {
            'src': 'my-src',
            'dist': 'my-dist',
            'app_name': 'foo'
        }

        file = io.StringIO()
        state.dump(file, config)

        file.seek(0)
        self.assertEqual(json.load(file), config)

    def test_load(self):
        """
        Test the load function.
        """
        config = {
            'src': 'my-src',
            'dist': 'my-dist',
            'app_name': 'foo'
        }

        file = io.StringIO(json.dumps(config))
        res = state.load(file)
        self.assertEqual(res, config)
