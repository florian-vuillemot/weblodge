"""
Based on Zip Deploy: https://learn.microsoft.com/en-us/azure/app-service/deploy-zip?tabs=cli

The output generates a zip file containing
- The user application code.
- The user application requirements.
- A generated Kudu deployment configuration file.
- A generated startup file.

This package is ready to be deployed on an Azure Web App.
"""
from dataclasses import dataclass
import os
from pathlib import Path
from typing import List
import zipfile

from weblodge.config import Item as ConfigItem


@dataclass(frozen=True)
class Build:
    """
    Facade to the build process.

    User-customizable fields are found in the `config` property. All are optional from the user's
    point of view so build can proceed without any configuration.
    """
    # Source directory to zip.
    src: str = '.'
    # Destination directory to the zip file `name`.
    dist: str = 'dist'
    # Application entrypoint.
    entry_point: str = 'app.py'
    # Flask application object.
    app: str = 'app'

    # Zip file that contains the user application code.
    package: str = 'azwebapp.zip'
    # Kudu deployment config file.
    kudu_config: str = '.deployment'
    # Startup file.
    startup_file: str = 'startup.txt'

    @property
    def package_path(self) -> str:
        """
        Return the package path.
        """
        return os.path.join(self.dist, self.package)

    @classmethod
    @property
    def config(cls) -> List[ConfigItem]:
        """
        Return the build configuration.
        """
        return [
            ConfigItem(
                name='src',
                description='Application folder.',
                default=cls.src
            ),
            ConfigItem(
                name='dist',
                description='Build destination.',
                default=cls.dist
            ),
            ConfigItem(
                name='entry_point',
                description='Application entry point.',
                default=cls.entry_point
            ),
            ConfigItem(
                name='app',
                description='Flask Application object.',
                default=cls.app
            )
        ]

    def build(self) -> None:
        """
        Build an application to a deployable format.
        """
        # Create the destination directory.
        os.makedirs(self.dist, exist_ok=True)

        # Zip all required files together.
        with zipfile.ZipFile(self.package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            self._zip_user_application(zipf)
            self._deployment_config(zipf)
            self._startup_file(zipf)

    def _zip_user_application(self, zipf: zipfile.ZipFile):
        """
        Create the zip folder.
        """
        for root, _, files in os.walk(self.src):
            root = Path(root)
            # Skip hidden files and directories.
            if root.name.startswith('.'):
                continue
            # Skip bytecode files.
            if '__pycache__' in root.name:
                continue
            # Skip the build directory.
            if root.is_relative_to(self.dist):
                continue
            # Zip the files.
            for file in files:
                file_path = root / file
                relative_to = file_path.relative_to(self.src)
                zipf.write(file_path, relative_to)

    def _deployment_config(self, zipf: zipfile.ZipFile):
        """
        Add the deployment config file to the zip folder.
        """
        # Kudu deployment config file.
        config = '''\
[config]
# Packages must be installed using during the deployment build.
SCM_DO_BUILD_DURING_DEPLOYMENT = true
'''
        # Add the deployment config file to the zip folder.
        zipf.writestr(
            os.path.relpath(self.kudu_config, self.src),
            config
        )

    def _startup_file(self, zipf: zipfile.ZipFile):
        """
        Add the startup file to the zip folder.
        """
        # Remove potentional .py extension.
        entrypoint = self.entry_point
        if entrypoint.endswith('.py'):
            entrypoint = entrypoint[:-3]

        # Add the application object if it's not already there.
        if ':' not in entrypoint:
            entrypoint = f'{entrypoint}:{self.app}'

        # Default application configuration update with the user and entrypoint.
        # https://learn.microsoft.com/en-us/azure/developer/python/configure-python-web-app-on-app-service
        startup_file_content = f'gunicorn --bind=0.0.0.0 --timeout 600 {entrypoint}'

        # Add the startup file to the zip folder.
        zipf.writestr(
            os.path.relpath(self.startup_file, self.src),
            startup_file_content
        )
