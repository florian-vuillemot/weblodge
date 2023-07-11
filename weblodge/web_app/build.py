"""
Based on Zip Deploy: https://learn.microsoft.com/en-us/azure/app-service/deploy-zip?tabs=cli

The output generates a zip file containing
- The user application code.
- The user application requirements.
- A generated Kudu deployment configuration file.
- A generated startup file.

This package is ready to be deployed on an Azure Web App.
"""
import os
from pathlib import Path
from typing import List
import zipfile

from weblodge.config import Item as ConfigItem


class BuildException(Exception):
    """
    Build exception.
    """


class RequirementsFileNotFound(BuildException):
    """
    The requirements file was not found.
    """


class BuildConfig:
    """
    Build configuration.

    User-customizable fields are found in the `config` property. All are optional from the user's
    point of view so build can proceed without any configuration.
    """
    # Zip file that contains the user application code.
    package: str = 'azwebapp.zip'
    # Kudu deployment config file.
    kudu_config: str = '.deployment'
    # Startup file.
    # Set in the deployment config too.
    startup_file: str = 'weblodge.startup'
    # Kudu needs a requirements file at the root of the zip.
    kudu_requirements_path = 'requirements.txt'

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        src: str,
        dist: str,
        entry_point: str,
        app: str,
        requirements: str,
        *_args,
        **_kwargs
    ):
        # Source directory to zip.
        self.src = src
        # Destination directory to the zip file `name`.
        self.dist = dist
        # Application entrypoint.
        self.entry_point = entry_point
        # Flask application object.
        self.app = app
        # User requirements file.
        self.requirements = requirements

    @property
    def package_path(self) -> str:
        """
        Return the package path.
        """
        return os.path.join(self.dist, self.package)

    @classmethod
    @property
    def items(cls) -> List[ConfigItem]:
        """
        Items that can be configured.
        """
        return [
            ConfigItem(
                name='src',
                description='Application folder.',
                default='.'
            ),
            ConfigItem(
                name='dist',
                description='Build destination.',
                default='dist'
            ),
            ConfigItem(
                name='entry_point',
                description='Application entry point.',
                default='app.py'
            ),
            ConfigItem(
                name='app',
                description='Flask Application object.',
                default='app'
            ),
            ConfigItem(
                name='requirements',
                description='Requirements.txt file path.',
                default='requirements.txt'
            )
        ]


def build(config: BuildConfig) -> None:
    """
    Build an application to a deployable format.
    """
    # Create the destination directory.
    os.makedirs(config.dist, exist_ok=True)

    # Zip all required files together.
    with zipfile.ZipFile(config.package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        requirements_file_included = _zip_user_application(config, zipf)
        _deployment_config(config, zipf)
        _startup_file(config, zipf)

        # Add the requirements file if it was not included in the user application folder.
        if not requirements_file_included:
            _requirements(config, zipf)


def _zip_user_application(config: BuildConfig, zipf: zipfile.ZipFile) -> bool:
    """
    Create the zip folder.

    Return True if the requirements file was included at the root of the application folder.
    """
    requirements_file_included = False

    for root, _, files in os.walk(config.src):
        root = Path(root)
        # Skip hidden files and directories.
        if root.name.startswith('.'):
            continue
        # Skip bytecode files.
        if '__pycache__' in root.name:
            continue
        # Skip the build directory.
        # Path conversion removes unnecessary slashes.
        if root.name.startswith(Path(config.dist).name):
            continue
        # Zip the files.
        for file in files:
            file_path = root / file
            relative_to = os.path.relpath(file_path, config.src)

            zipf.write(file_path, relative_to)

            if not requirements_file_included:
                # If the requirements file is not already included at the root of the application
                # folder, check if the current file is that one.
                requirements_file_included = Path(relative_to) == Path(config.kudu_requirements_path)

    return requirements_file_included


def _requirements(config: BuildConfig, zipf: zipfile.ZipFile):
    """
    Add the requirements file to the zip folder from the user folder.
    """
    if not os.path.exists(config.requirements):
        raise RequirementsFileNotFound()

    zipf.write(config.requirements, config.kudu_requirements_path)


def _deployment_config(config: BuildConfig, zipf: zipfile.ZipFile):
    """
    Add the deployment config file to the zip folder.
    """
    # Kudu deployment config file.
    kudu_config = '''\
[config]
# Packages must be installed using during the deployment build.
SCM_DO_BUILD_DURING_DEPLOYMENT = true
'''
    # Add the deployment config file to the zip folder.
    zipf.writestr(config.kudu_config, kudu_config)


def _startup_file(config: BuildConfig, zipf: zipfile.ZipFile):
    """
    Add the startup file to the zip folder.
    """
    # Remove potentional .py extension.
    entrypoint = config.entry_point
    if entrypoint.endswith('.py'):
        entrypoint = entrypoint[:-3]

    # Add the application object if it's not already there.
    if ':' not in entrypoint:
        entrypoint = f'{entrypoint}:{config.app}'

    # Default application configuration update with the user and entrypoint.
    # https://learn.microsoft.com/en-us/azure/developer/python/configure-python-web-app-on-app-service
    startup_file_content = f'gunicorn --bind=0.0.0.0 --timeout 600 {entrypoint}'

    # Add the startup file to the zip folder.
    zipf.writestr(config.startup_file, startup_file_content)
