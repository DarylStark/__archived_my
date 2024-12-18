""" Module that contains the methods to get and set user details from
    the database. """

from typing import List, Optional, Union

import sqlalchemy
from sqlalchemy.orm.query import Query

from database import DatabaseSession
from my_database import logger, validate_input
from my_database.exceptions import (FilterNotValidError, IntegrityError,
                                    NotFoundError, PermissionDeniedError)
from my_database.field import Field
from my_database_model import User, UserRole

# Define the fields for validation
validation_fields = {
    'fullname': Field(
        'fullname',
        str,
        str_regex_validator=r'[A-Za-z0-9\- ]+'),
    'username': Field(
        'username',
        str,
        str_regex_validator=r'[A-Za-z][A-Za-z0-9\-_.]+'),
    'email': Field(
        'email',
        str,
        str_regex_validator=r'[a-z0-9_\-.]+@[a-z.-]+\.[a-z.]+'),
    'role': Field('role', UserRole),
    'password': Field('password', str),
    'secret': Field('secret', str)
}


def create_user(req_user: User, **kwargs: dict) -> Optional[User]:
    """" Method to create a user

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what the user is allowed to do.

        **kwargs : dict
            A dict containing the fields for the user.

        Returns
        -------
        User
            The created user object.

        None
            The user was not created.
    """

    # Set the needed fields
    required_fields = {
        'fullname': validation_fields['fullname'],
        'username': validation_fields['username'],
        'email': validation_fields['email'],
        'role': validation_fields['role']
    }

    # Set the optional fields
    optional_fields = None

    # Validate the user input
    validate_input(
        input_values=kwargs,
        required_fields=required_fields,
        optional_fields=optional_fields)

    logger.debug('create_user: all arguments are validated')

    # Combine the arguments
    all_fields: dict = dict()
    if required_fields:
        all_fields.update(required_fields)
    if optional_fields:
        all_fields.update(optional_fields)

    # Normal users cannot create users, admin users can only create
    # normal and admin users. Root can create whatever it wants.
    if (req_user.role == UserRole.user):
        raise PermissionDeniedError(
            'A user with role "user" cannot create users')
    elif (req_user.role == UserRole.admin and
            kwargs['role'] == UserRole.root):
        raise PermissionDeniedError(
            'A user with role "admin" can only create admin and normal users')

    logger.debug('create_user: user is authorized')

    try:
        with DatabaseSession(
            commit_on_end=True,
            expire_on_commit=False
        ) as session:
            # Create the resource
            new_resource = User()

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

            # Set a password for this user
            new_resource.set_random_password()

            logger.debug('create_user: adding user')

            # Add the resource
            session.add(new_resource)

            # Return the created resource
            return new_resource
    except sqlalchemy.exc.IntegrityError as sa_error:
        logger.error(f'create_user: IntegrityError: {str(sa_error)}')
        # Add a custom text to the exception
        raise IntegrityError('User already exists') from sa_error

    return None


def get_users(
    req_user: User,
    flt_id: Optional[int] = None,
    flt_username: Optional[str] = None
) -> Optional[Union[List[User], User]]:
    """ Method that retrieves all, or a subset of, the users in the
        database.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what results the user gets.

        flt_id : Optional[int] [default=None]
            Filter on a specific user ID.

        flt_username : Optional[str] [default=None]
            Filter on a specific username.

        Returns
        -------
        List[User]
            A list with the resulting users.

        User
            The found user (if filtered on a uniq value, like flt_id).

        None
            No users are found.
    """

    # Empty data list
    data_list: Optional[Query] = None
    rv: Optional[List[User]] = None

    # Get the resources
    with DatabaseSession(commit_on_end=False, expire_on_commit=False) \
            as session:
        # First, we get all users
        data_list = session.query(User)

        # Then, we check the role that this user has. 'Root' users can
        # retrieve all users. Admin users can retrieve normal and admin
        # users. Normal users can only retrieve themselves.
        role = req_user.role

        if role == UserRole.admin:
            # Admin role: only sees other admins and other users
            data_list = data_list.filter(User.role != UserRole.root)
        elif role == UserRole.user:
            # Normal user: only sees it's own profile
            if not flt_id or flt_id == req_user.id:
                data_list = data_list.filter(User.id == req_user.id)
            else:
                raise NotFoundError(
                    f'User with ID {flt_id} is not found.')

        logger.debug('get_users: we have the global list of users')

        # Apply filter for ID
        try:
            if flt_id:
                flt_id = int(flt_id)
                data_list = data_list.filter(User.id == flt_id)
                logger.debug('get_users: list is filtered')
        except (ValueError, TypeError):
            logger.error(
                f'User id should be of type {int}, not {type(flt_id)}.')
            raise FilterNotValidError(
                f'User id should be of type {int}, not {type(flt_id)}.') from None

        # Apply filter for username
        if flt_username:
            flt_username = flt_username
            data_list = data_list.filter(User.username == flt_username)
            logger.debug('get_users: list is filtered on username')

        # Get the data
        if flt_id:
            rv = data_list.first()
            if rv is None:
                raise NotFoundError(
                    f'User with ID {flt_id} is not found.')
        elif flt_username:
            rv = data_list.first()
            if rv is None:
                raise NotFoundError(
                    f'User with username "{flt_username}" is not found.')
        else:
            rv = data_list.all()
            if len(rv) == 0:
                logger.debug('get_users: no users to return')
                rv = None

    # Return the data
    logger.debug('get_users: returning users')
    return rv


def update_user(
    req_user: User,
    user_id: int,
    **kwargs: dict
) -> Optional[User]:
    """ Method to update a user.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what the user is allowed to do.

        user_id : int
            The ID for the user to change

        **kwargs : dict
            A dict containing the fields for the user.

        Returns
        -------
        User
            The updated user object.

        None
            No user updated.
    """

    # Get the resource object
    resource: Optional[Union[List[User], User]] = \
        get_users(req_user, flt_id=user_id)

    logger.debug('update_user: we have the resource')

    # Set the needed fields
    required_fields = None

    # Set the optional fields
    optional_fields = {
        'fullname': validation_fields['fullname'],
        'username': validation_fields['username'],
        'email': validation_fields['email'],
        'role': validation_fields['role']
    }

    # Validate the user input
    validate_input(
        input_values=kwargs,
        required_fields=required_fields,
        optional_fields=optional_fields)

    logger.debug('update_user: all arguments are validated')

    # Combine the arguments
    all_fields: dict = dict()
    if required_fields:
        all_fields.update(required_fields)
    if optional_fields:
        all_fields.update(optional_fields)

    # Authorize this request; check if the user requesting this is
    # allowed to change the role of the user
    if 'role' in kwargs.keys():
        if req_user.role == UserRole.user and resource != req_user:
            raise PermissionDeniedError(
                'A user with role "user" can only change his own useraccount')
        elif req_user.role == UserRole.admin:
            if kwargs['role'] == UserRole.root:
                raise PermissionDeniedError(
                    'A user with role "admin" cannot elevate users to the ' +
                    'role of "root"')

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
            logger.debug('update_user: merging resource into session')

            # Add the changed resource to the session
            session.merge(resource)

        # Done! Return the resource
        if isinstance(resource, User):
            logger.debug('update_user: updating was a success!')
            return resource
    except sqlalchemy.exc.IntegrityError as sa_error:
        # Add a custom text to the exception
        logger.error(
            f'update_user: sqlalchemy.exc.IntegrityError: {str(sa_error)}')
        raise IntegrityError('User already exists') from sa_error

    return None


def update_user_password(
    req_user: User,
    user_id: int,
    **kwargs: dict
) -> Optional[User]:
    """ Method to update the password of a user.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what the user is allowed to do.

        user_id : int
            The ID for the user to change

        **kwargs : dict
            A dict containing the fields for the user.

        Returns
        -------
        User
            The updated user object.

        None
            No user updated.
    """

    # Get the resource object
    resource: Optional[Union[List[User], User]] = \
        get_users(req_user, flt_id=user_id)

    logger.debug('update_user_password: we have the resource')

    # Set the needed fields
    required_fields = {
        'password': validation_fields['password']
    }

    # Set the optional fields
    optional_fields = None

    # Validate the user input
    validate_input(
        input_values=kwargs,
        required_fields=required_fields,
        optional_fields=optional_fields)

    logger.debug('update_user_password: all arguments are validated')

    # Combine the arguments
    all_fields: dict = dict()
    if required_fields:
        all_fields.update(required_fields)
    if optional_fields:
        all_fields.update(optional_fields)

    # Authorize this request; a 'normal' user can change the password of his
    # own account. A admin can change the password of every 'normal' account
    # and the root user can change all passwords
    if req_user.role == UserRole.user and req_user.id != resource.id:
        raise PermissionDeniedError(
            'A user with role "user" can only change his own password')
    elif (req_user.role == UserRole.admin and
            (resource.role != UserRole.user or
             resource.role != UserRole.admin)
          ):
        raise PermissionDeniedError(
            'A user with role "admin" can only change the password for normal users and admins')

    logger.debug('create_user: user is authorized')

    # Update the password
    logger.debug('update_user_password :: setting password')
    resource.set_password(kwargs['password'])

    # Save the fields
    try:
        with DatabaseSession(
            commit_on_end=True,
            expire_on_commit=True
        ) as session:
            logger.debug('update_user_password: merging resource into session')

            # Add the changed resource to the session
            session.merge(resource)

        # Done! Return the resource
        if isinstance(resource, User):
            logger.debug('update_user_password: updating was a success!')
            return resource
    except sqlalchemy.exc.IntegrityError as sa_error:
        # Add a custom text to the exception
        logger.error(
            f'update_user_password: sqlalchemy.exc.IntegrityError: {str(sa_error)}')
        raise IntegrityError('User already exists') from sa_error

    return None


def update_user_2fa_secret(
    req_user: User,
    user_id: int,
    **kwargs: dict
) -> Optional[User]:
    """ Method to update the 2FA for a user.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what the user is allowed to do.

        user_id : int
            The ID for the user to change

        **kwargs : dict
            A dict containing the fields for the user.

        Returns
        -------
        User
            The updated user object.

        None
            No user updated.
    """

    # Get the resource object
    resource: Optional[Union[List[User], User]] = \
        get_users(req_user, flt_id=user_id)

    logger.debug('update_user_2fa_secret: we have the resource')

    # Set the needed fields
    required_fields = {
        'secret': validation_fields['secret']
    }

    # Set the optional fields
    optional_fields = None

    # Validate the user input
    validate_input(
        input_values=kwargs,
        required_fields=required_fields,
        optional_fields=optional_fields)

    logger.debug('update_user_2fa_secret: all arguments are validated')

    # Combine the arguments
    all_fields: dict = dict()
    if required_fields:
        all_fields.update(required_fields)
    if optional_fields:
        all_fields.update(optional_fields)

    # It is only allowed to set the secret for your own account
    if req_user.id != resource.id:
        raise PermissionDeniedError(
            'You can only set the secret for your own account')

    logger.debug('update_user_2fa_secret: user is authorized')

    # Update the secret
    logger.debug('update_user_2fa_secret :: setting secret')
    resource.set_second_factor(kwargs['secret'])

    # Save the fields
    try:
        with DatabaseSession(
            commit_on_end=True,
            expire_on_commit=True
        ) as session:
            logger.debug(
                'update_user_2fa_secret: merging resource into session')

            # Add the changed resource to the session
            session.merge(resource)

        # Done! Return the resource
        if isinstance(resource, User):
            logger.debug('update_user_2fa_secret: updating was a success!')
            return resource
    except sqlalchemy.exc.IntegrityError as sa_error:
        # Add a custom text to the exception
        logger.error(
            f'update_user_2fa_secret: sqlalchemy.exc.IntegrityError: {str(sa_error)}')
        raise IntegrityError('User already exists') from sa_error

    return None


def update_user_disable_2fa(
    req_user: User,
    user_id: int
) -> Optional[User]:
    """ Method to disable 2FA for a user.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what the user is allowed to do.

        user_id : int
            The ID for the user to change

        Returns
        -------
        User
            The updated user object.

        None
            No user updated.
    """

    # Get the resource object
    resource: Optional[Union[List[User], User]] = \
        get_users(req_user, flt_id=user_id)

    logger.debug('update_user_disable_2fa: we have the resource')

    # It is only allowed to set the secret for your own account
    if req_user.id != resource.id:
        raise PermissionDeniedError(
            'You can only disable 2FA for your own account')

    logger.debug('update_user_disable_2fa: user is authorized')

    # Update the password
    logger.debug('update_user_2fa_secret :: setting secret')
    resource.disable_second_factor()

    # Save the fields
    try:
        with DatabaseSession(
            commit_on_end=True,
            expire_on_commit=True
        ) as session:
            logger.debug(
                'update_user_2fa_secret: merging resource into session')

            # Add the changed resource to the session
            session.merge(resource)

        # Done! Return the resource
        if isinstance(resource, User):
            logger.debug('update_user_2fa_secret: updating was a success!')
            return resource
    except sqlalchemy.exc.IntegrityError as sa_error:
        # Add a custom text to the exception
        logger.error(
            f'update_user_2fa_secret: sqlalchemy.exc.IntegrityError: {str(sa_error)}')
        raise IntegrityError('User already exists') from sa_error

    return None


def delete_user(
    req_user: User,
    user_id: int
) -> bool:
    """ Method to delete a user.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what the user is allowed to do.

        user_id : int
            The ID for the user to delete.

        Returns
        -------
        bool
            True on success.
    """

    # If a 'normal' user is requesting this, we fail immidiatly
    if req_user.role == UserRole.user:
        raise PermissionDeniedError(
            'A user with role "user" cannot delete users')

    # Get the user
    resource = get_users(req_user=req_user, flt_id=user_id)

    logger.debug('delete_user: we have the resource')

    # A user cannot remove itself
    if req_user.id == user_id:
        raise PermissionDeniedError(
            'You cannot remove your own user account')
    elif (req_user.role == UserRole.admin and resource.role == UserRole.root):
        raise PermissionDeniedError(
            'A admin cannot remove root users')

    # Create a database session
    try:
        with DatabaseSession(
            commit_on_end=True,
            expire_on_commit=True
        ) as session:
            # Delete the resource
            logger.debug('delete_user: deleting the resource')
            session.delete(resource)
    except sqlalchemy.exc.IntegrityError as sa_error:
        logger.error(
            f'delete_user: sqlalchemy.exc.IntegrityError: {str(sa_error)}')
        raise IntegrityError(
            'User couldn\'t be deleted because it still has resources ' +
            'connected to it') from sa_error
    else:
        logger.debug('delete_user: return True because it was a success')
        return True
