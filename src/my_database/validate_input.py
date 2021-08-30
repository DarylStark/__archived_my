"""
    Module that contains the 'validate_input' function which can and
    should be used to validate input from the user.
"""

from re import fullmatch
from typing import Dict, Optional
from my_database.exceptions import FieldNotValidatedError
from my_database.field import Field


def validate_input(
        input_values: dict,
        required_fields: Optional[dict] = None,
        optional_fields: Optional[dict] = None):
    """
        Function to validate input

        Parameters
        ----------
        input_values : dict
            The data the user has given.

        required_fields : Optional[dict] [default=None]
            Dict with 'Field' objects to indicate what fields are
            required.

        optional_fields : Optional[dict] [default=None]
            Dict with 'Field' objects to indicate what fields are
            optional.

        Returns
        -------
        bool
            True if all fields are validated
    """
    # Combine the 'needed' and 'optional' fields
    all_fields: Dict[str, Field] = dict()
    if required_fields:
        all_fields.update(required_fields)
    if optional_fields:
        all_fields.update(optional_fields)

    # Check if no other unexpected keys are given
    for field in input_values.keys():
        if field not in all_fields:
            raise TypeError(
                f'Unexpected field "{field}"')

    # Check if we have all required fields
    if required_fields:
        for field in required_fields.keys():
            if field not in input_values.keys():
                raise TypeError(
                    f'Missing required argument "{field}"')

    # Check if the given fields are of the correct type
    for field, value in input_values.items():
        # Get the validators
        expected_data_type = all_fields[field].datatype

        # Validate the type
        if type(value) is not expected_data_type:
            raise TypeError(
                f'{field} should be of type {expected_data_type}, ' +
                f'not {type(value)}.')

        # Validate the field - strings
        if type(value) is str:
            regex = all_fields[field].str_regex_validator
            if regex:
                if not fullmatch(regex, value):
                    raise FieldNotValidatedError(
                        f'Value "{value}" is not valid for "{field}"')

    # Everything is validated
    return True
