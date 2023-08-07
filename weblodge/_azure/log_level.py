"""
Log levels set to the Azure WebApp.
"""

from .interfaces import AzureLogLevel


class LogLevel(AzureLogLevel):
    """
    Log levels.
    By default, the log level is set to Warning.
    """
    def __init__(self) -> None:
        self._log_level = 'warning'

    def to_azure(self) -> str:
        """
        Convert in Azure values.
        """
        return self._log_level

    def error(self) -> None:
        """
        Set the log level to error.
        """
        self._log_level = 'error'

    def information(self) -> None:
        """
        Set the log level to information.
        """
        self._log_level = 'information'

    def verbose(self) -> None:
        """
        Set the log level to verbose.
        """
        self._log_level = 'verbose'

    def warning(self) -> None:
        """
        Set the log level to warning.
        """
        self._log_level = 'warning'
