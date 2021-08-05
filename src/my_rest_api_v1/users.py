"""
    Module that has the RESTAPIGroup for the 'users' group of the API.
    This group can be used to get user information.
"""
from random import random
import re
from typing import Optional
from flask import request
from my_database.exceptions import IntegrityError, MyDatabaseError
from my_database.generic import create_object
from my_database.users import get_users
from my_database_model import User
from my_database_model.user import UserRole
from rest_api_generator import Authorization, Group, Response, ResponseType
from rest_api_generator.endpoint_scopes import EndpointScopes
from rest_api_generator.exceptions import (ResourceForbiddenError,
                                           ResourceIntegrityError,
                                           ResourceNotFoundError)
import string
import random

api_group_users = Group(
    api_url_prefix='users',
    name='users',
    description='Contains endpoints for users'
)


@api_group_users.register_endpoint(
    url_suffix=['user'],
    http_methods=['POST'],
    name='user',
    description='Endpoint to create a user',
    auth_needed=True,
    auth_scopes=EndpointScopes(POST=['users.create'])
)
def users_create(auth: Optional[Authorization],
                 url_match: re.Match) -> Response:
    """
        REST API Endpoint '/users/user'. Creates a tag.

        Parameters
        ----------
        auth : RESTAPIAuthorization
            A object that contains authorization information.

        url_match : re.Match
            Endpoint that contains the regex match object that was used
            to match the URL.

        Returns
        -------
        RESTAPIResponse
            The API response
    """

    # Create a RESTAPIResponse object
    return_response = Response(ResponseType.SINGLE_RESOURCE)

    # Set the data
    try:
        # Get the data
        post_data = request.json

        # Check if we have all fields
        needed_fields = [
            'fullname', 'username', 'email',
            'role'
        ]
        for field in needed_fields:
            if field not in post_data.keys():
                raise ResourceNotFoundError(
                    f'Field "{field}" missing in request')

        # Normal users cannot create users, admin users can only create
        # normal users. Root can create whatever he wants.
        if (auth.data.user.role == UserRole.user):
            raise ResourceForbiddenError('A user cannot create users')
        elif (auth.data.user.role == UserRole.admin and
              post_data['role'] != 'user'):
            raise ResourceForbiddenError(
                'A admin can only create normal users')

        # Create a user
        new_object = User(
            fullname=post_data['fullname'],
            username=post_data['username'],
            email=post_data['email'],
            role=post_data['role'],
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
            raise ResourceIntegrityError('User already exists')
        else:
            return_response.data = new_object

    except MyDatabaseError:
        raise ResourceNotFoundError

    # Return the create RESTAPIResponse object
    return return_response


@api_group_users.register_endpoint(
    url_suffix=['users', 'users/', 'users/([0-9]+)'],
    http_methods=['GET'],
    name='users',
    description='Endpoint to retrieve all or a subset of the users',
    auth_needed=True,
    auth_scopes=EndpointScopes(GET=['users.retrieve'])
)
def users_retrieve(auth: Optional[Authorization],
                   url_match: re.Match) -> Response:
    """
        REST API Endpoing '/users/users'. Returns a list with users.

        Parameters
        ----------
        auth : RESTAPIAuthorization
            A object that contains authorization information.

        url_match : re.Match
            Endpoint that contains the regex match object that was used
            to match the URL.

        Returns
        -------
        RESTAPIResponse
            The API response
    """

    # Create a RESTAPIResponse object
    return_response = Response(ResponseType.RESOURCE_SET)

    # Set the data
    try:
        # Check if we received a ID
        user_id = None
        if len(url_match.groups()) > 0:
            user_id = int(url_match.groups(0)[0])
            return_response.type = ResponseType.SINGLE_RESOURCE

        # Get the users
        return_response.data = get_users(
            auth.data.user,
            flt_id=user_id
        )

        if len(return_response.data) == 0 and user_id is not None:
            raise ResourceNotFoundError('Not a valid user ID')

        # If the user requested only one resource, we only put that
        # resource in the return
        if user_id is not None:
            return_response.data = return_response.data[0]
    except MyDatabaseError:
        raise ResourceNotFoundError

    # Return the create RESTAPIResponse object
    return return_response
