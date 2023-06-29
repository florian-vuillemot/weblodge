from dataclasses import dataclass, field
import os
import zipfile

from weblodge.config import ConfigField


@dataclass
class Build:
    # Source directory to zip.
    src: str = '.'
    # Destination directory to the zip file `name`.
    dest: str = 'dist'

    # Zip file that contains the user application code.
    package: str = 'azwebapp.zip'
    # Kudu deployment config file.
    kudu_config: str = '.deployment'

    @property
    def package_path(self) -> str:
        """
        Return the package path.
        """
        return os.path.join(self.dest, self.package)

    @classmethod
    def config(cls):
        return [
            ConfigField(
                name='src',
                description='Application folder.',
                example='.',
                default=cls.src
            ),
            ConfigField(
                name='dest',
                description='Build destination.',
                example='dist',
                default=cls.dest
            )
        ]

    def build(self) -> None:
        """
        Build an application to a deployable format.
        """
        # Create the destination directory.
        os.makedirs(self.dest, exist_ok=True)

        with zipfile.ZipFile(self.package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            self._zip_user_application(zipf)
            self._add_deployment_config(zipf)

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
            if root.startswith(self.dest) or root.startswith('./' + self.dest) or root.startswith('.\\' + self.dest):
                continue
            # Zip the files.
            for file in files:
                file_path = os.path.join(root, file)
                relative_to = os.path.relpath(file_path, self.src)
                zipf.write(file_path, relative_to)

    def _add_deployment_config(self, zipf: zipfile.ZipFile):
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
