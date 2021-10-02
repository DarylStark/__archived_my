""" Module that contains the functions to authorize users based on
    their credentials. """

from typing import List, Optional
from my_database.field import Field
from database import DatabaseSession
from my_database import validate_input
from my_database_model import User
from my_database import logger
from my_database.exceptions import (AuthUserRequiresSecondFactorError,
                                    AuthCredentialsError)

# Define the fields for validation
validation_fields = {
    'username': Field(
        'username',
        str,
        str_regex_validator=r'^[A-Za-z0-9_\.\-]+$'),
    'password': Field(
        'password',
        str,
        str_regex_validator=r'^.+$'),
    'second_factor': Field(
        'second_factor',
        str,
        str_regex_validator=r'^\d{6}$')
}


def validate_credentials(**kwargs: dict) -> Optional[User]:
    """" Method to vaidate user credentials

        Parameters
        ----------
        **kwargs : dict
            A dict containing the fields for the authorization
            validation.

        Returns
        -------
        User
            The created API token object.

        None
            The authorization request failed.
    """

    # Set the needed fields
    required_fields = {
        'username': validation_fields['username'],
        'password': validation_fields['password'],
    }

    # Set the optional fields
    optional_fields = {
        'second_factor': validation_fields['second_factor']
    }

    # Validate the user input
    validate_input(
        input_values=kwargs,
        required_fields=required_fields,
        optional_fields=optional_fields)

    logger.debug('validate_credentials: all arguments are validated')

    # Combine the arguments
    all_fields: dict = dict()
    if required_fields:
        all_fields.update(required_fields)
    if optional_fields:
        all_fields.update(optional_fields)

    # Get the user object
    with DatabaseSession(commit_on_end=False, expire_on_commit=False) \
            as session:
        data_list = session.query(User).filter(
            User.username == kwargs['username'])

        if data_list.count() != 1:
            # Check what we got; if we didn't found a user, we raise a
            # AuthUserNotFoundError exception, so the calling function
            # can do the appropiate actions
            raise AuthCredentialsError(
                f'A user with username "{kwargs["username"]}" was not found')

        # If we have a user with a matching username, we check if
        # this user requires a 'second factor' authentication code,
        # or just the password
        user: User = data_list.first()
        second_factor_needed = user.second_factor is not None

    if second_factor_needed and 'second_factor' not in kwargs.keys():
        # Second factor is needed, but not given. We raise an
        # error, so the calling function can do the appropiate
        # actions
        raise AuthUserRequiresSecondFactorError(
            f'User "{kwargs["username"]}" needs a second factor, ' +
            'but none was given')
    else:
        # Second factor is needed and also provided or a second factor
        # is not needed. We can verify the users credentials
        if not user.verify_credentials(
            password=kwargs['password'],
            second_factor=kwargs.get('second_factor', None)
        ):
            # Credentials were not correct. Error!
            raise AuthCredentialsError(
                f'The password or second factor for user "{user.username}" were not correct')

    # Credentials are correct! We return the user object
    return user
