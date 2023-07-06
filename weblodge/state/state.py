# pylint: disable=missing-module-docstring
import json


def dump(name_or_fd, config):
    """
    Dump the config to a file or file descriptor.
    """
    if isinstance(name_or_fd, str):
        with open(name_or_fd, 'w', encoding='utf-8') as file_descriptor:
            json.dump(config, file_descriptor, indent=4)
    else:
        json.dump(config, name_or_fd, indent=4)


def load(name_or_fd):
    """
    Load the config from a file or file descriptor.
    """
    try:
        if isinstance(name_or_fd, str):
            with open(name_or_fd, 'r', encoding='utf-8') as file_descriptor:
                return json.load(file_descriptor)
        else:
            return json.load(name_or_fd)
    except FileNotFoundError:
        return {}
