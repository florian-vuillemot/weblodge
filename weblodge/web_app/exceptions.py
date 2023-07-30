"""
Web App exceptions.
"""
class BuildException(Exception):
    """
    Exception relative to the build.
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


class DeploymentException(Exception):
    """
    Exception relative to the deployment.
    """


class FreeApplicationAlreadyDeployed(DeploymentException):
    """
    A free application is already deployed.
    Contains the name of the free application.
    """
