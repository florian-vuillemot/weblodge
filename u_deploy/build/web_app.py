import os
import zipfile
from pathlib import Path


def build(name: str, src: Path = Path('.'), dest: Path = Path('build')) -> None:
    """
    Build an application to a deployable format.
    """
    # Create the destination directory.
    dest.mkdir(parents=True, exist_ok=True)

    fp_zip = Path(f'{dest / name}.zip')

    src = str(src)
    dest = str(dest)

    with zipfile.ZipFile(fp_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(src):
            # Skip hidden files and directories.
            if '/.' in root or '\\.' in root:
                continue

            # Skip bytecode files.
            if '__pycache__' in root:
                continue

            # Skip the build directory.
            if root.startswith(dest) or root.startswith('./' + dest) or root.startswith('.\\' + dest):
                continue

            # Zip the files.
            for file in files:
                file_path = os.path.join(root, file)
                relative_to = os.path.relpath(os.path.join(root, file), src)
                zipf.write(file_path, relative_to)
