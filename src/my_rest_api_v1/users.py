"""
    Module that has the RESTAPIGroup for the 'users' group of the API.
    This group can be used to get user information.
"""
import re
from typing import Optional
from flask import request
from my_database.exceptions import (IntegrityError, MyDatabaseError,
                                    PermissionDeniedError)
from my_database.users import create_user, get_users, update_user
from my_database_model import User
from my_database_model.user import UserRole
from rest_api_generator import Authorization, Group, Response, ResponseType
from rest_api_generator.endpoint_scopes import EndpointScopes
from rest_api_generator.exceptions import (ResourceForbiddenError,
                                           ResourceIntegrityError,
                                           ResourceNotFoundError, ServerError)

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
        REST API Endpoint '/users/user'. Creates a user.

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

    # TODO: Check if no other fields are given

    # Transform the role
    roles = {
        'user': UserRole.user,
        'admin': UserRole.admin,
        'root': UserRole.root
    }
    role: UserRole = UserRole.user
    if post_data['role'] in roles.keys():
        role = roles[post_data['role']]
    else:
        raise ResourceNotFoundError(
            f'Role "{post_data["role"]}" is not a valid role')

    # Create the user
    try:
        new_object = create_user(
            req_user=auth.data.user,
            fullname=post_data['fullname'],
            username=post_data['username'],
            email=post_data['email'],
            role=role
        )
    except PermissionDeniedError as err:
        # Permission denied errors happen when a user tries to add
        # a type of user he is not allowed to create.
        raise ResourceForbiddenError(err)
    except IntegrityError as err:
        # Integrity errors happen mostly when the user already
        # exists.
        raise ResourceIntegrityError(err)
    except Exception as err:
        # Every other error should result in a ServerError.
        raise ServerError(err)
    else:
        # If nothing went wrong, return the newly created object.
        return_response.data = new_object

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
        resource_id = None
        if len(url_match.groups()) > 0:
            resource_id = int(url_match.groups(0)[0])
            return_response.type = ResponseType.SINGLE_RESOURCE

        # Get the resources
        return_response.data = get_users(
            auth.data.user,
            flt_id=resource_id
        )

        # Check if we received data
        if len(return_response.data) == 0 and resource_id is not None:
            raise ResourceNotFoundError('Not a valid user ID')

        # If the user requested only one resource, we only put that
        # resource in the return
        if resource_id is not None:
            return_response.data = return_response.data[0]
    except MyDatabaseError:
        raise ResourceNotFoundError

    # Return the create RESTAPIResponse object
    return return_response


@api_group_users.register_endpoint(
    url_suffix=['user/([0-9]+)'],
    http_methods=['PATCH', 'DELETE'],
    name='user',
    description='Endpoint to edit or delete a user',
    auth_needed=True,
    auth_scopes=EndpointScopes(
        PATCH=['users.update'],
        DELETE=['users.delete']
    )
)
def users_update_delete(auth: Optional[Authorization],
                        url_match: re.Match) -> Response:
    """
        REST API Endpoint '/users/user/([0-9]+)'. Edits or deletes a user.

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

    # Get the user ID
    resource_id = int(url_match.groups(0)[0])

    # Update user
    if request.method == 'PATCH':
        # Get the data
        post_data = request.json

        # Check if we received the correct fields
        optional_fields = [
            'fullname', 'username', 'email',
            'role'
        ]
        for field in post_data.keys():
            if field not in optional_fields:
                raise ResourceNotFoundError(
                    f'Field "{field}" is not a valid field for this request')

        # Transform the role to a role that fits the `my_database`
        # better.
        if 'role' in post_data.keys():
            roles = {
                'user': UserRole.user,
                'admin': UserRole.admin,
                'root': UserRole.root
            }
            if post_data['role'] in roles.keys():
                post_data['role'] = roles[post_data['role']]
            else:
                raise ResourceNotFoundError(
                    f'Role "{post_data["role"]}" is not a valid role')

        # Update the user
        try:
            changed_resource = update_user(
                req_user=auth.data.user,
                user_id=resource_id,
                **post_data
            )
        except PermissionDeniedError as err:
            # Permission denied errors happen when a user tries to add
            # a type of user he is not allowed to create.
            raise ResourceForbiddenError(err)
        except IntegrityError as err:
            # Integrity errors happen mostly when the user already
            # exists.
            raise ResourceIntegrityError(err)
        except Exception as err:
            # Every other error should result in a ServerError.
            raise ServerError(err)
        else:
            # If nothing went wrong, return the newly created object.
            return_response.data = changed_resource

    # Delete user
    if request.method == 'DELETE':
        raise NotImplementedError('not yet implemented')

    # Return the create RESTAPIResponse object
    return return_response
