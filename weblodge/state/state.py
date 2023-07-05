import json
import pathlib


def dump(name_or_fd, config):
    """
    Dump the config to a file or file descriptor.
    """
    if isinstance(name_or_fd, str):
        with open(name_or_fd, 'w') as fd:
            json.dump(config, fd, indent=4)
    else:
        json.dump(config, name_or_fd, indent=4)


def load(name_or_fd):
    """
    Load the config from a file or file descriptor.
    """
    try:
        if isinstance(name_or_fd, str):
            with open(name_or_fd, 'r') as fd:
                return json.load(fd)
        else:
            return json.load(name_or_fd)
    except FileNotFoundError:
        return {}


def delete(name):
    """
    Delete the state file if exists.
    """
    pathlib.Path(name).unlink(missing_ok=True)
