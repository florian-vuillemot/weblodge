"""
User inputs can be provided by command line.
This package contains the logic to parse the command line arguments for internal
components based on the configuration items. but also the global arguments that are
hard coded.

The help method must be adapted to the action to be carried out.
Examples:
    `python weblodge.py -h` must print the `help` message of **WebLodge**.
    `python weblodge.py build -h` must print the `help` message for the `build` action.
"""
from .parameters import Parser, ConfigIsDefined, ConfigIsNotDefined
