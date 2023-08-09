"""
Log Level Tests.
"""
import unittest

from weblodge._azure.log_level import LogLevel


class TestLogLevel(unittest.TestCase):
    """
    Log Level tests.
    """
    def test_set_error(self):
        """
        Test error level.
        """
        log_level = LogLevel()
        log_level.error()

        self.assertEqual(log_level.to_azure(), 'error')

    def test_set_information(self):
        """
        Test information level.
        """
        log_level = LogLevel()
        log_level.information()

        self.assertEqual(log_level.to_azure(), 'information')

    def test_set_verbose(self):
        """
        Test verbose level.
        """
        log_level = LogLevel()
        log_level.verbose()

        self.assertEqual(log_level.to_azure(), 'verbose')

    def test_set_warning(self):
        """
        Test warning level.
        """
        log_level = LogLevel()
        log_level.warning()

        self.assertEqual(log_level.to_azure(), 'warning')
