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
import zipfile

from weblodge.config import Item as ConfigItem

from .exceptions import RequirementsFileNotFound, EntryPointFileNotFound, FlaskAppNotFound


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

    # Configurable items of the build.
    items = [
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
            name='flask_app',
            description='The Flask application object.',
            default='app'
        ),
        ConfigItem(
            name='requirements',
            description='Requirements.txt file path.',
            default='requirements.txt'
        )
    ]

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        src: str,
        dist: str,
        entry_point: str,
        flask_app: str,
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
        self.flask_app = flask_app
        # User requirements file.
        self.requirements = requirements

    @property
    def package_path(self) -> str:
        """
        Return the package path.
        """
        return os.path.join(self.dist, self.package)


def build(config: BuildConfig) -> None:
    """
    Build an application to a deployable format.
    """
    # Create the destination directory.
    os.makedirs(config.dist, exist_ok=True)

    # Zip all required files together.
    with zipfile.ZipFile(config.package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        _user_application(config, zipf)
        _user_requirements(config, zipf)
        _deployment_config(config, zipf)
        _startup_file(config, zipf)


def _user_application(config: BuildConfig, zipf: zipfile.ZipFile):
    """
    Create the zip folder.
    """
    # The requirements file name.
    # It will be added to the zip folder in a dedicated function.
    # If it is added twice, the ZIP library prints an error.
    requirements_filename = Path(config.requirements).name

    # Ensure the entry point exists.
    entry_point = Path(config.src) / config.entry_point
    if not entry_point.exists():
        raise EntryPointFileNotFound()

    # Ensure the flask app is in the entry point file.
    if config.flask_app not in entry_point.read_text():
        raise FlaskAppNotFound()

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

            # Skip the requirements file.
            if relative_to == requirements_filename:
                continue

            zipf.write(file_path, relative_to)


def _user_requirements(config: BuildConfig, zipf: zipfile.ZipFile):
    """
    Add the requirements file to the zip folder from the user folder.
    The file can be in the local folder or in the `src` folder.
    """
    if os.path.exists(config.requirements):
        zipf.write(config.requirements, config.kudu_requirements_path)
        return

    requirements_in_src = Path(config.src) / config.requirements
    if requirements_in_src.exists():
        zipf.write(requirements_in_src, config.kudu_requirements_path)
        return

    raise RequirementsFileNotFound()


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
        entrypoint = f'{entrypoint}:{config.flask_app}'

    # Default application configuration update with the user and entrypoint.
    # https://learn.microsoft.com/en-us/azure/developer/python/configure-python-web-app-on-app-service
    startup_file_content = f'gunicorn --bind=0.0.0.0 --timeout 600 {entrypoint}'

    # Add the startup file to the zip folder.
    zipf.writestr(config.startup_file, startup_file_content)
