from dataclasses import dataclass
import os
from typing import List
import zipfile

from weblodge.config import Item as ConfigItem


@dataclass(frozen=True)
class Build:
    # Source directory to zip.
    src: str = '.'
    # Destination directory to the zip file `name`.
    dist: str = 'dist'
    # Application entrypoint.
    entrypoint: str = 'app.py'
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
                name='entrypoint',
                description='Application entrypoint.',
                default=cls.entrypoint
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

        with zipfile.ZipFile(self.package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            self._zip_user_application(zipf)
            self._deployment_config(zipf)
            self._startup_file(zipf)

    def _zip_user_application(self, zipf: zipfile.ZipFile):
        """
        Create the zip folder.
        """
        for root, _, files in os.walk(self.src):
            # Skip hidden files and directories.
            if '/.' in root or '\\.' in root:
                continue
            # Skip bytecode files.
            if '__pycache__' in root:
                continue
            # Skip the build directory.
            if root.startswith(self.dist) or root.startswith('./' + self.dist) or root.startswith('.\\' + self.dist):
                continue
            # Zip the files.
            for file in files:
                file_path = os.path.join(root, file)
                relative_to = os.path.relpath(file_path, self.src)
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
        # Skip the startup file if the entrypoint is a default supported values.
        if self.entrypoint in ('app.py', 'application.py', 'app', 'application') and self.app == 'app':
            return

        # Remove potentional .py extension.
        entrypoint = self.entrypoint
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
