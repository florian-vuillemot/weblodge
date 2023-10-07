"""
Web App exceptions.
"""
class BuildException(Exception):
    """
    Exceptions relative to the build.
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
    Exceptions relative to the deployment.
    """


class NoMoreFreeApplicationAvailable(DeploymentException):
    """
    A free application is already deployed.
    Contains the name of the free application.
    """


class InvalidTier(DeploymentException):
    """
    Can not find the asked tier.
    """


class AppTierException(Exception):
    """
    Exceptions relative to the app-tier command.
    """


class CanNotFindTierLocation(AppTierException):
    """
    Can not find any tier for the provided location.
    """
