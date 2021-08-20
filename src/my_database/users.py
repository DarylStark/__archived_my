"""
    Module that contains the methods to get and set user details from
    the database.
"""
import random
import string
from typing import List, Optional, Union
import sqlalchemy
from database import DatabaseSession
from my_database_model import User, UserRole
from sqlalchemy.orm.query import Query
from my_database import logger
from my_database.exceptions import (FilterNotValidError,
                                    IntegrityError, PermissionDeniedError,
                                    NotFoundError)
from rest_api_generator.exceptions import ServerError


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

    """

    # Check if we have al the needed fields
    needed_fields = [
        'fullname', 'username', 'email',
        'role'
    ]

    for field in needed_fields:
        if field not in kwargs.keys():
            raise TypeError(
                f'Missing required argument "{field}"')

    # TODO: Check if no other fields are given

    # Normal users cannot create users, admin users can only create
    # normal users. Root can create whatever he wants.
    if (req_user.role == UserRole.user):
        raise PermissionDeniedError(
            'A user with role "user" cannot create users')
    elif (req_user.role == UserRole.admin and
            kwargs['role'] != UserRole.user):
        raise PermissionDeniedError(
            'A user with role "admin" can only create normal users')

    try:
        with DatabaseSession(
            commit_on_end=True,
            expire_on_commit=True
        ) as session:
            # Create the resource
            new_resource = User(
                fullname=kwargs['fullname'],
                username=kwargs['username'],
                email=kwargs['email'],
                role=kwargs['role'],
            )

            # Generate a random password for this user
            characters = string.ascii_letters
            characters += string.digits
            characters += string.punctuation
            length = random.randint(24, 33)
            random_password = [random.choice(characters)
                               for i in range(0, length)]
            random_password = ''.join(random_password)

            # Set the password for the user
            new_resource.set_password(random_password)

            # Add the resource
            session.add(new_resource)

            # Return the created resource
            return new_resource
    except IntegrityError:
        # Add a custom text to the exception
        raise IntegrityError('User already exists')
    except Exception as e:
        raise ServerError(e)

    return None


def get_users(
    req_user: User,
    flt_id: Optional[int] = None
) -> Optional[Union[List[User], User]]:
    """ Method that retrieves all, or a subset of, the users in the
        database.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what results the user gets.

        flt_id : Optional[int]
            Filter on a specific user ID.

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

    # Get the token
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

        # Now, we can apply the correct filters
        try:
            if flt_id:
                flt_id = int(flt_id)
                data_list = data_list.filter(User.id == flt_id)
        except (ValueError, TypeError):
            logger.error(
                f'User id should be of type {int}, not {type(flt_id)}.')
            raise FilterNotValidError(
                f'User id should be of type {int}, not {type(flt_id)}.')

        # Get the data
        if flt_id:
            rv = data_list.first()
            if rv is None:
                raise NotFoundError(
                    f'User with ID {flt_id} is not found.')
        else:
            rv = data_list.all()
            if len(rv) == 0:
                rv = None

    # Return the data
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

    # TODO: Check if no 'weird' fields are given

    # Check if the context user can change the requested user. Normal
    # users cannot change any users, admin users can only change normal
    # users and admin users. Root users can change everything.
    if (req_user.role == UserRole.user):
        raise PermissionDeniedError(
            'A user with role "user" cannot change users')
    elif (req_user.role == UserRole.admin and
            resource.role == UserRole.root):
        raise PermissionDeniedError(
            'A user with role "admin" can only change normal users')

    # Set the variables that are updatable
    fields = {
        'fullname': 'fullname',
        'username': 'username',
        'email': 'email',
        'role': 'role'
    }

    # Update the resource
    for field in kwargs.keys():
        if field in fields.keys():
            setattr(resource, fields[field], kwargs[field])
        else:
            raise FilterNotValidError(
                f'Field {field} is not a valid field')

    # Save the fields
    try:
        with DatabaseSession(
            commit_on_end=True,
            expire_on_commit=True
        ) as session:
            # Add the changed resource to the session
            session.merge(resource)

        # Done! Return the resource
        if isinstance(resource, User):
            return resource
    except sqlalchemy.exc.IntegrityError:
        # Add a custom text to the exception
        raise IntegrityError('User already exists')

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

    # Create a database session
    try:
        with DatabaseSession(
            commit_on_end=True,
            expire_on_commit=True
        ) as session:
            # A user cannot remove itself
            if req_user.id == user_id:
                raise PermissionDeniedError(
                    'You cannot remove your own user account')

            # Delete the resource
            session.delete(resource)
    except sqlalchemy.exc.IntegrityError:
        raise ServerError(
            'User couldn\'t be deleted because it still has resources ' +
            'connected to it')
    else:
        return True
