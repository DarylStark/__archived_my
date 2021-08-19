"""
    Module that contains the methods to get and set user details from
    the database.
"""
import random
import string
from typing import List, Optional, Type
from database import DatabaseSession
from my_database.clients import delete_api_client
from my_database.tags import delete_tag
from my_database.tokens import delete_token
from my_database_model import User, UserRole
from sqlalchemy.orm.query import Query
from my_database import logger
from my_database.exceptions import (FilterNotValidError,
                                    IntegrityError, PermissionDeniedError,
                                    ResourceNotFoundError)
from my_database.generic import create_object, delete_object, update_object


def create_user(req_user: User, **kwargs: dict) -> User:
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

    # Create a user
    new_object = User(
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
    random_password = [random.choice(characters) for i in range(0, length)]
    random_password = ''.join(random_password)

    # Set the password for the user
    new_object.set_password(random_password)

    # Add the object
    try:
        create_object(new_object)
    except IntegrityError:
        # Add a custom text to the exception
        raise IntegrityError('User already exists')
    else:
        return new_object


def get_users(
    req_user: User,
    flt_id: Optional[int] = None
) -> Optional[List[User]]:
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
        # retrieve all users. Admin users can retrieve
        role = req_user.role

        if role == UserRole.admin:
            # Admin role: only sees other admins and other users
            data_list = data_list.filter(User.role != UserRole.root)
        elif role == UserRole.user:
            # Normal user: only sees it's own profile
            if not flt_id or flt_id == req_user.id:
                data_list = data_list.filter(User.id == req_user.id)
            else:
                return None

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
        if data_list is not None:
            rv = data_list.all()

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
    """

    # Get the resource object
    resource: Optional[List[User]] = get_users(req_user, flt_id=user_id)

    # TODO: Check if no 'weird' fields are given

    # Check if we got a resource. If we didn't, we rise an error
    # indicating that the resource wasn't found. This can be either
    # because it didn't exist, or because the user has no permissions
    # to it.
    if resource is None or len(resource) == 0:
        raise ResourceNotFoundError(f'User with ID {user_id} is not found.')

    # Appeaently we have resources. Because the result is a list, we
    # we can assume the first one in the list is the one we are
    # interested in.
    resource = resource[0]

    # Check if the context user can change the requested user. Normal
    # users cannot change any users, admin users can only change normal
    # users and root users can change everything.
    if (req_user.role == UserRole.user):
        raise PermissionDeniedError(
            'A user with role "user" cannot change users')
    elif (req_user.role == UserRole.admin and
            resource.role != UserRole.user):
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
        update_object(resource)
    except IntegrityError:
        # Add a custom text to the exception
        raise IntegrityError('User already exists')
    else:
        return resource


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

    # Get the resource object
    resource: Optional[List[User]] = get_users(req_user, flt_id=user_id)

    # Check if we got a resource. If we didn't, we rise an error
    # indicating that the resource wasn't found. This can be either
    # because it didn't exist, or because the user has no permissions
    # to it.
    if resource is None or len(resource) == 0:
        raise ResourceNotFoundError(f'User with ID {user_id} is not found.')

    # Appearently we have resources. Because the result is a list, we
    # we can assume the first one in the list is the one we are
    # interested in.
    resource = resource[0]

    # Check if the context user can delete the requested user. Normal
    # users cannot delete any users, admin users can only delete normal
    # users and root users can delete everything.
    if (req_user.role == UserRole.user):
        raise PermissionDeniedError(
            'A user with role "user" cannot delete users')
    elif (req_user.role == UserRole.admin and
            resource.role != UserRole.user):
        raise PermissionDeniedError(
            'A user with role "admin" can only delete normal users')

    # Delete the resource
    try:
        # Before we can delete the resource, we have to get the
        # resources that are connected to this resource.
        # Delete all connected tags
        for connected_resource in [rs for rs in resource.tags]:
            # Remove the connected resource
            delete_tag(
                req_user=None,
                tag_id=connected_resource.id)

            # Remove it from the resource
            resource.tags.remove(connected_resource)

        # Delete all connected tokens
        for connected_resource in [rs for rs in resource.tokens]:
            # Remove the connected resource
            delete_token(req_user, connected_resource.id)

            # Remove it from the resource
            resource.tokens.remove(connected_resource)

        # Delete all connected clients
        for connected_resource in [rs for rs in resource.clients]:
            # Remove the connected resource
            delete_api_client(req_user, connected_resource.id)

            # Remove it from the resource
            resource.clients.remove(connected_resource)

        # Finally, delete the resource itself
        delete_object(resource)
    except IntegrityError:
        # Add a custom text to the exception
        raise IntegrityError(
            'User couldn\'t be deleted because it still has resources ' +
            'connected to it')
    else:
        return True
