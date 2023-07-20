"""
Web App exceptions.
"""
class BuildException(Exception):
    """
    Build exception.
    """


class RequirementsFileNotFound(BuildException):
    """
    The requirements file was not found.
    """


class EntryPointFileNotFound(BuildException):
    """
    The entry point file was not found.
    """


class FlaskAppNotFound(BuildException):
    """
    Can not find the Flask application object in the entry point file.
    """
