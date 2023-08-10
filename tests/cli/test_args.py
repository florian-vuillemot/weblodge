"""
Test CLI arguments parsing.
"""
import sys
import unittest

from weblodge.cli.args import get_cli_args, DEFAULT_CONFIG_FILE


class TestCliArgs(unittest.TestCase):
    """
    CLI arguments parsing.
    """
    def test_action(self):
        """
        The action parameter is required and must be parsed.
        """
        sys.argv = [sys.argv[0], 'build']

        action, config_filename = get_cli_args()
        self.assertEqual(action, 'build')
        self.assertEqual(config_filename, DEFAULT_CONFIG_FILE)

    def test_failed_when_action_is_missing(self):
        """
        The action parameter is required, if not provided, error must be returned.
        """
        sys.argv = [sys.argv[0]]

        with self.assertRaises(SystemExit):
            get_cli_args()

    def test_config_file(self):
        """
        The config file can be provided.
        """
        filename = 'my-config-file'

        sys.argv = [sys.argv[0], 'deploy', '--config-file', filename]

        action, config_filename = get_cli_args()
        self.assertEqual(action, 'deploy')
        self.assertEqual(config_filename, filename)
