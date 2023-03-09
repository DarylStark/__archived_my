""" Module that contains the functions to authorize users based on
    their credentials. """

from typing import List, Optional, Union
import sqlalchemy
from my_database.field import Field
from database import DatabaseSession
from my_database import validate_input
from my_database_model import User, UserSession
from my_database import logger
from sqlalchemy.orm.query import Query
from my_database.exceptions import (AuthUserRequiresSecondFactorError,
                                    AuthCredentialsError, FilterNotValidError, IntegrityError, NotFoundError)

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
        str_regex_validator=r'^\d{6}$'),
    'host': Field(
        'host',
        str,
        str_regex_validator=r'^[a-f0-9\.\:]+$'),
    'session_id': Field(
        'session_id',
        int),
    'title': Field(
        'title',
        str,
        str_regex_validator=r'^[A-Za-z0-9\ \-\._]*$'),
    'session_ids': Field(
        'session_ids',
        list)
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


def create_user_session(req_user: User, **kwargs: dict) -> Optional[UserSession]:
    """" Method to create a user session

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what the user is allowed to do.

        **kwargs : dict
            A dict containing the fields for the authorization
            validation.

        Returns
        -------
        UserSession
            The created user session object.

        None
            The user session was not created.
    """

    # Set the needed fields
    required_fields = {
        'host': validation_fields['host']
    }

    # Set the optional fields
    optional_fields = None

    # Validate the user input
    validate_input(
        input_values=kwargs,
        required_fields=required_fields,
        optional_fields=optional_fields)

    logger.debug('create_user_session: all arguments are validated')

    # Combine the arguments
    all_fields: dict = dict()
    if required_fields:
        all_fields.update(required_fields)
    if optional_fields:
        all_fields.update(optional_fields)

    try:
        with DatabaseSession(
            commit_on_end=True,
            expire_on_commit=False
        ) as session:
            # Create the resource
            new_resource = UserSession()

            # Set the fields
            for field in kwargs.keys():
                if field in all_fields.keys():
                    if hasattr(new_resource, all_fields[field].object_field):
                        setattr(
                            new_resource,
                            all_fields[field].object_field,
                            kwargs[field])
                    else:
                        raise AttributeError(
                            f"'{type(new_resource)}' has no attribute " +
                            f"'{all_fields[field].object_field}'"
                        )
                else:
                    raise FilterNotValidError(
                        f'Field {field} is not a valid field')

            # Set the User ID
            new_resource.user = req_user

            # Set a secret
            new_resource.set_random_secret()

            logger.debug('create_user_session: adding user session')

            # Add the resource
            session.add(new_resource)

            # Return the created resource
            return new_resource
    except sqlalchemy.exc.IntegrityError as sa_error:
        logger.error(f'create_user_session: IntegrityError: {str(sa_error)}')
        # Add a custom text to the exception
        raise IntegrityError('UserSession already exists') from sa_error

    return None


def get_user_sessions(
    req_user: Optional[User],
    flt_id: Optional[int] = None
) -> Optional[Union[List[UserSession], UserSession]]:
    """ Method that retrieves all, or a subset of, the userssessions in
        the database.

        Parameters
        ----------
        req_user : Optional[User]
            The user who is requesting this. Should be used to verify
            what results the user gets. If this is set to None, we the
            function retrieves all user sessions.

        flt_id : Optional[int] [default=None]
            Filter on a specific usersession ID.

        Returns
        -------
        List[UserSession]
            A list with the resulting sessions.

        User
            The found sessions (if filtered on a uniq value, like
            flt_id).

        None
            No sessions are found.
    """

    # Empty data list
    data_list: Optional[Query] = None
    rv: Optional[List[UserSession]] = None

    # Get the resources
    with DatabaseSession(commit_on_end=False, expire_on_commit=False) \
            as session:
        # First, we get all sessions
        data_list = session.query(UserSession)

        # Then, we filter on the sessions to only show the sessions
        # that this user is allowed to see. We only do that is a
        # `req_user` is given
        if req_user:
            data_list = data_list.filter(UserSession.user == req_user)

        logger.debug('get_user_sessions: we have the list of users')

        # Apply filter for ID
        try:
            if flt_id:
                flt_id = int(flt_id)
                data_list = data_list.filter(UserSession.id == flt_id)
                logger.debug('get_user_sessions: list is filtered')
        except (ValueError, TypeError):
            logger.error(
                f'UserSession id should be of type {int}, not {type(flt_id)}.')
            raise FilterNotValidError(
                f'UserSession id should be of type {int}, not {type(flt_id)}.') from None

        # Get the data
        if flt_id:
            rv = data_list.first()
            if rv is None:
                raise NotFoundError(
                    f'User session with ID {flt_id} is not found.')
        else:
            rv = data_list.all()
            if len(rv) == 0:
                logger.debug('get_user_sessions: no usersessions to return')
                rv = None

    # Return the data
    logger.debug('get_user_sessions: returning userssessions')
    return rv


def update_user_session(
    req_user: User,
    user_session_id: int,
    **kwargs: dict
) -> Optional[UserSession]:
    """ Method to update a user session.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what the user is allowed to do.

        user_session_id : int
            The ID for the user session to change

        **kwargs : dict
            A dict containing the fields for the session.

        Returns
        -------
        UserSession
            The updated user session object.

        None
            No user session updated.
    """

    # Get the resource object
    resource: Optional[Union[List[UserSession], UserSession]] = \
        get_user_sessions(req_user, flt_id=user_session_id)

    logger.debug('update_user_session: we have the resource')

    # Set the needed fields
    required_fields = {
        'title': validation_fields['title']
    }

    # Set the optional fields
    optional_fields = None

    # Validate the user input
    validate_input(
        input_values=kwargs,
        required_fields=required_fields,
        optional_fields=optional_fields)

    logger.debug('update_user_session: all arguments are validated')

    # Combine the arguments
    all_fields: dict = dict()
    if required_fields:
        all_fields.update(required_fields)
    if optional_fields:
        all_fields.update(optional_fields)

    # Set the title to None if it is an empty string. This way, we can make sure
    # that no real empty strings get saved
    if kwargs['title'] == '':
        kwargs['title'] = None

    # Update the resource
    for field in kwargs.keys():
        if field in all_fields.keys():
            if hasattr(resource, all_fields[field].object_field):
                setattr(
                    resource,
                    all_fields[field].object_field,
                    kwargs[field])
            else:
                raise AttributeError(
                    f"'{type(resource)}' has no attribute " +
                    f"'{all_fields[field].object_field}'"
                )
        else:
            raise FilterNotValidError(
                f'Field {field} is not a valid field')

    # Save the fields
    try:
        with DatabaseSession(
            commit_on_end=True,
            expire_on_commit=True
        ) as session:
            logger.debug('update_user_session: merging resource into session')

            # Add the changed resource to the session
            session.merge(resource)

        # Done! Return the resource
        if isinstance(resource, UserSession):
            logger.debug('update_user_session: updating was a success!')
            return resource
    except sqlalchemy.exc.IntegrityError as sa_error:
        # Add a custom text to the exception
        logger.error(
            f'update_user_session: sqlalchemy.exc.IntegrityError: {str(sa_error)}')
        raise IntegrityError('UserSession already exists') from sa_error

    return None


def delete_user_sessions(
    req_user: User,
    session_id: Union[List[int], int]
) -> bool:
    """ Method to delete a user session.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what the user is allowed to do.

        session_id : Union[List[int], int]
            A list of sessions to delete or a session ID

        Returns
        -------
        bool
            True on success.
    """

    # Get the user sessions
    resources = None
    if type(session_id) is list:
        resources = [
            get_user_sessions(req_user=req_user, flt_id=r)
            for r in session_id
        ]
    else:
        resources = [get_user_sessions(req_user=req_user, flt_id=session_id)]

    logger.debug('delete_user_sessions: we have the resources')

    # Create a database session
    try:
        with DatabaseSession(
            commit_on_end=True,
            expire_on_commit=True
        ) as session:
            # Delete the resource
            logger.debug('delete_user_sessions: deleting the resources')
            for resource in resources:
                session.delete(resource)
    except sqlalchemy.exc.IntegrityError as sa_error:
        logger.error(
            f'delete_user_sessions: sqlalchemy.exc.IntegrityError: {str(sa_error)}')
        raise IntegrityError(
            'Session couldn\'t be deleted because it still has resources ' +
            'connected to it') from sa_error
    else:
        logger.debug(
            'delete_user_sessions: return True because it was a success')
        return True
