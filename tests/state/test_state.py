import io
import json
import unittest

import weblodge.state as state


class TestState(unittest.TestCase):
    def test_dump(self):
        config = {
            'src': 'my-src',
            'dist': 'my-dist',
            'app_name': 'foo'
        }
        fd = io.StringIO()
        state.dump(fd, config)
        fd.seek(0)
        self.assertEqual(json.load(fd), config)

    def test_load(self):
        config = {
            'src': 'my-src',
            'dist': 'my-dist',
            'app_name': 'foo'
        }
        fd = io.StringIO(json.dumps(config))
        res = state.load(fd)
        self.assertEqual(res, config)
