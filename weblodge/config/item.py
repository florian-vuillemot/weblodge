"""
A configuration item represents information about a function that can be
overwritten at runtime.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Item:
    """
    Information that can be overwritten at runtime.
    """
    # Name of the field.
    # This name will be used as the command line argument, in the code and config files.
    name: str
    # Description of the field. What is it used for?
    description: str
    # Does not expect a value from the user. The argument is a flag.
    # Example: --verbose
    attending_value: bool = True
    # Default value of the field.
    # When specified, the field is optional.
    default: Optional[str] = None
    # List of possible values.
    values_allowed: Optional[list] = None

    def __eq__(self, obj) -> bool:
        if isinstance(obj, Item):
            return self.name == obj.name
        if isinstance(obj, str):
            return self.name == obj
        return False
