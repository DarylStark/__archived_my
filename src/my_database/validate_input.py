"""
    Module that contains the 'validate_input' function which can and
    should be used to validate input from the user.
"""


from typing import Optional


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
    all_fields: dict = dict()
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
        expected_data_type = all_fields[field].datatype
        if type(value) is not expected_data_type:
            raise TypeError(
                f'{field} should be of type {expected_data_type}, ' +
                f'not {type(value)}.')

    # Everything is validated
    return True
