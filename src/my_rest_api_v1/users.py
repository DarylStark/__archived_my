"""
    Module that has the RESTAPIGroup for the 'users' group of the API.
    This group can be used to get user information.
"""
import re
from typing import Optional
from flask import request
from my_database.exceptions import (IntegrityError, MyDatabaseError,
                                    NotFoundError, PermissionDeniedError)
from my_database.users import create_user, delete_user, get_users, update_user
from my_database_model.user import UserRole
from rest_api_generator import Authorization, Group, Response, ResponseType
from rest_api_generator.endpoint_scopes import EndpointScopes
from rest_api_generator.exceptions import (InvalidInputError, ResourceForbiddenError,
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
            raise InvalidInputError(
                f'Field "{field}" missing in request')

    # Check if no other fields are given

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
        raise InvalidInputError(
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

    # Return the created RESTAPIResponse object
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
    except NotFoundError as err:
        # Resource not found happens when a user tries to change a
        # user that does not exists
        raise ResourceNotFoundError(err)
    except Exception as err:
        # Every other error should result in a ServerError.
        raise ServerError(err)

    # Return the created RESTAPIResponse object
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
                raise InvalidInputError(
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
                raise InvalidInputError(
                    f'Role "{post_data["role"]}" is not a valid role')

        # Update the user
        try:
            changed_resource = update_user(
                req_user=auth.data.user,
                user_id=resource_id,
                **post_data
            )
        except PermissionDeniedError as err:
            # Permission denied errors happens when a user tries to
            # change a type of user he is not allowed to create.
            raise ResourceForbiddenError(err)
        except NotFoundError as err:
            # Resource not found happens when a user tries to change a
            # user that does not exists
            raise ResourceNotFoundError(err)
        except IntegrityError as err:
            # Integrity errors happen mostly when the user already
            # exists.
            raise ResourceIntegrityError(err)
        except Exception as err:
            # Every other error should result in a ServerError.
            raise ServerError(err)

        # If nothing went wrong, return the newly created object.
        return_response.data = changed_resource

    # Delete user
    if request.method == 'DELETE':
        try:
            delete_user(
                req_user=auth.data.user,
                user_id=resource_id
            )
        except PermissionDeniedError as err:
            # Permission denied errors happen when a user tries to
            # delete a type of resource he is not allowed to delete.
            raise ResourceForbiddenError(err)
        except NotFoundError as err:
            # Resource not found happens when a user tries to delete a
            # user that does not exists
            raise ResourceNotFoundError(err)
        except IntegrityError as err:
            # Integrity errors happen mostly when the resource has
            # connections to other resources that should be deleted
            # first.
            raise ResourceIntegrityError(err)
        except Exception as err:
            # Every other error should result in a ServerError.
            raise ServerError(err)
        else:
            # If nothing went wrong, we create a object with the key
            # 'deleted' that we return to the client.
            return_response.data = {
                'deleted': True
            }

    # Return the created RESTAPIResponse object
    return return_response
