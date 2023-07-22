"""
Retrieve parameters of the application.

Currently, the parameters are retrieved from the command line.
"""
import argparse

from dataclasses import dataclass
from typing import Callable, Dict, List

from weblodge.config import Item as ConfigItem


@dataclass(frozen=True, eq=False)
class _ConfigTrigger(ConfigItem):
    """
    Configuration Item with a function to trigger.
    Can only be defined in the meta configuration.
    """
    # Function to call.
    trigger: Callable[[Dict[str, str]], Dict[str, str]] = None


@dataclass(frozen=True, eq=False)
class ConfigIsDefined(_ConfigTrigger):
    """
    Call the trigger if the user provides the parameter.
    """


@dataclass(frozen=True, eq=False)
class ConfigIsNotDefined(_ConfigTrigger):
    """
    Call the trigger if the user does not provide the parameter.
    """


class Parser:
    """
    Parse the command line arguments.

    Function(s) can be triggered if the user provides the right arguments.
    They will run only onces and their config will not be added to the global config.
    Example:
    ```
    def _build(config):
        print('Build the application.')
        return config
    parser = Parser()
    parser.trigger_once(
        ConfigTrigger(name='build', description='Build the application.', trigger=_build)
    )
    # If the user runs: `python weblodge.py build -h` then the help message will contain
    # the `build` option.
    # If the user runs: `python weblodge.py build` then the `_build` function will be called
    # but the config will not contains the 'build' item.
    parser.load(config)
    ```
    """
    def __init__(self) -> None:
        self._triggers: List[_ConfigTrigger] = []

    def load(self, fields: List[ConfigItem], existing_parameters: Dict[str, str] = None) -> Dict[str, str]:
        """
        Load the configuration from the parser.
        Override the current config with the new values.
        """
        existing_parameters = existing_parameters or {}

        # Create and configure a parser for the fields.
        parser = argparse.ArgumentParser()
        for field in fields + self._triggers:
            argument = {
                'help': field.description,
            }

            default_value = existing_parameters.get(field.name, field.default)

            if not field.attending_value:
                argument['action'] = 'store_true'
            else:
                argument = {
                    **argument,
                    'type': str,
                    'required': default_value is None,
                    'default': default_value,
                }

            parser.add_argument(
                f'--{_to_display(field.name)}',
                **argument
            )
        args_parsed, _ = parser.parse_known_args()
        new_config = vars(args_parsed)

        # Expected configuration must not contains configuration used for intermediate
        # operations.
        _complete_config = {**existing_parameters, **new_config}
        config = {k: v for k, v in _complete_config.items() if k not in self._triggers}

        # Trigger meta configs functions.
        while self._triggers:
            # Trigger are removes from the list as they are called
            # to avoid infinite recursion.
            _config = self._triggers.pop()
            if _config.attending_value:
                # If a value is expected, check if the user provided it.
                is_defined = _config.name in new_config
            else:
                # If no value is expected, the attending value will create
                # fill the config with False.
                is_defined = new_config[_config.name]

            if is_defined and isinstance(_config, ConfigIsDefined):
                config = _config.trigger(config)
            elif not is_defined and isinstance(_config, ConfigIsNotDefined):
                config = _config.trigger(config)

        return config

    def trigger_once(self, trigger: _ConfigTrigger) -> 'Parser':
        """
        Add configuration trigger.
        Configuration defined will not be added to the config.
        This trigger will be analyse only once then remove from triggers.
        """
        self._triggers.append(trigger)


def _to_display(name: str) -> str:
    return name.replace('_', '-')
