"""
    Module that contains the Dataclass 'Field', which can be used to
    specify fields for the database methods.
"""

from dataclasses import dataclass
from typing import Optional, Type


@dataclass
class Field:
    """
        Object that contains a specific field that can be given to the
        database methods.

        Members
        -------
        object_field : str
            The field that it represents in the database

        datatype : Type
            The type that it should be

        str_regex_validator : Optional[str] [default=None]
            A regex that can be used to validate strings
    """
    object_field: str
    datatype: type
    str_regex_validator: Optional[str] = None
