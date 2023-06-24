from dataclasses import dataclass, field
import os
import zipfile


@dataclass
class WebApp:
    # Source directory to zip.
    src: str = field(default='.')
    # Destination directory to the zip file `name`.
    dest: str = field(default='dist')

    # Name of the zip file.
    name: str = 'azwebapp'
    # Kudu deployment config file
    kudu_config: str = '.deployment'

    def build(self) -> None:
        """
        Build an application to a deployable format.
        """
        # Create the destination directory.
        os.makedirs(self.dest, exist_ok=True)
        # Final zip file.
        fp_zip = os.path.join(self.dest, self.name) + '.zip'

        with zipfile.ZipFile(fp_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
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
