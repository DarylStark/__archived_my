""" Module that has the Group for the 'users' group of the API.
    This group can be used to get user information. """
import re
from typing import Optional

from flask import request

from my_database import validate_input
from my_database.exceptions import (FieldNotValidatedError, IntegrityError,
                                    NotFoundError, PermissionDeniedError)
from my_database.users import (create_user, delete_user, get_users,
                               update_user, validation_fields)
from my_database_model.user import UserRole
from rest_api_generator import Authorization, Group, Response, ResponseType
from rest_api_generator.endpoint_scopes import EndpointScopes
from rest_api_generator.exceptions import (InvalidInputError,
                                           ResourceForbiddenError,
                                           ResourceIntegrityError,
                                           ResourceNotFoundError, ServerError)

api_group_users = Group(
    api_url_prefix='users',
    name='users',
    description='Contains endpoints for users'
)


@api_group_users.register_endpoint(
    url_suffix=[
        r'user'
    ],
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
        auth : Authorization
            A object that contains authorization information.

        url_match : re.Match
            Endpoint that contains the regex match object that was used
            to match the URL.

        Returns
        -------
        Response
            The API response
    """

    # Create a Response object
    return_response = Response(ResponseType.SINGLE_RESOURCE)

    # Get the data
    post_data = request.json

    # Transform the role
    roles = {
        'user': UserRole.user,
        'admin': UserRole.admin,
        'root': UserRole.root
    }
    role: UserRole = UserRole.user
    if post_data['role'] in roles.keys():
        post_data['role'] = roles[post_data['role']]
    else:
        raise InvalidInputError(
            f'Role "{post_data["role"]}" is not a valid role')

    # Set the needed fields
    required_fields = {
        'fullname': validation_fields['fullname'],
        'username': validation_fields['username'],
        'email': validation_fields['email'],
        'role': validation_fields['role']
    }

    # Set the optional fields
    optional_fields = None

    try:
        # Validate the user input
        validate_input(
            input_values=post_data,
            required_fields=required_fields,
            optional_fields=optional_fields)
    except (TypeError, FieldNotValidatedError) as error:
        raise InvalidInputError(error) from None

    # Create the user
    try:
        new_object = create_user(
            req_user=auth.data.user,
            **post_data
        )
    except PermissionDeniedError as db_error:
        # Permission denied errors happen when a user tries to add
        # a type of user he is not allowed to create.
        raise ResourceForbiddenError(db_error) from db_error
    except IntegrityError as db_error:
        # Integrity errors happen mostly when the user already
        # exists.
        raise ResourceIntegrityError(db_error) from db_error
    except Exception as db_error:
        # Every other error should result in a ServerError.
        raise ServerError(db_error) from db_error
    else:
        # If nothing went wrong, return the newly created object.
        return_response.data = new_object

    # Return the created Response object
    return return_response


@api_group_users.register_endpoint(
    url_suffix=[
        r'users',
        r'users/',
        r'users/(?P<resource_id>[0-9]+)',
        r'users/(?P<resource_username>[A-Za-z][A-Za-z0-9\-_.]+)'
    ],
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
        auth : Authorization
            A object that contains authorization information.

        url_match : re.Match
            Endpoint that contains the regex match object that was used
            to match the URL.

        Returns
        -------
        Response
            The API response
    """

    # Create a Response object
    return_response = Response(ResponseType.RESOURCE_SET)

    # Set the data
    try:
        # Create a dict to send a filter to the database
        filters = {
            'flt_id': None,
            'flt_username': None
        }

        # Check if we received a ID
        if 'resource_id' in url_match.groupdict().keys():
            filters['flt_id'] = int(url_match.group('resource_id'))
            return_response.type = ResponseType.SINGLE_RESOURCE

        # Check if we received a username
        if 'resource_username' in url_match.groupdict().keys():
            filters['flt_username'] = url_match.group('resource_username')
            return_response.type = ResponseType.SINGLE_RESOURCE

        # Get the resources
        return_response.data = get_users(
            auth.data.user,
            **filters
        )
    except NotFoundError as db_error:
        # Resource not found happens when a user tries to get a
        # user that does not exists
        raise ResourceNotFoundError(db_error) from db_error
    except Exception as db_error:
        # Every other error should result in a ServerError.
        raise ServerError(db_error) from db_error

    # Return the created Response object
    return return_response


@api_group_users.register_endpoint(
    url_suffix=[
        r'user/([0-9]+)'
    ],
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
        auth : Authorization
            A object that contains authorization information.

        url_match : re.Match
            Endpoint that contains the regex match object that was used
            to match the URL.

        Returns
        -------
        Response
            The API response
    """

    # Create a Response object
    return_response = Response(ResponseType.SINGLE_RESOURCE)

    # Get the user ID
    resource_id = int(url_match.groups(0)[0])

    # Update user
    if request.method == 'PATCH':
        # Get the data
        post_data = request.json

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

        # Set the needed fields
        required_fields = None

        # Set the optional fields
        optional_fields = {
            'fullname': validation_fields['fullname'],
            'username': validation_fields['username'],
            'email': validation_fields['email'],
            'role': validation_fields['role']
        }

        try:
            # Validate the user input
            validate_input(
                input_values=post_data,
                required_fields=required_fields,
                optional_fields=optional_fields)
        except (TypeError, FieldNotValidatedError) as error:
            raise InvalidInputError(error) from None

        # Update the user
        try:
            changed_resource = update_user(
                req_user=auth.data.user,
                user_id=resource_id,
                **post_data
            )
        except PermissionDeniedError as db_error:
            # Permission denied errors happens when a user tries to
            # change a type of user he is not allowed to create.
            raise ResourceForbiddenError(db_error) from db_error
        except NotFoundError as db_error:
            # Resource not found happens when a user tries to change a
            # user that does not exists
            raise ResourceNotFoundError(db_error) from db_error
        except IntegrityError as db_error:
            # Integrity errors happen mostly when the user already
            # exists.
            raise ResourceIntegrityError(db_error) from db_error
        except Exception as db_error:
            # Every other error should result in a ServerError.
            raise ServerError(db_error) from db_error

        # If nothing went wrong, return the newly created object.
        return_response.data = changed_resource

    # Delete user
    if request.method == 'DELETE':
        try:
            delete_user(
                req_user=auth.data.user,
                user_id=resource_id
            )
        except PermissionDeniedError as db_error:
            # Permission denied errors happen when a user tries to
            # delete a type of resource he is not allowed to delete.
            raise ResourceForbiddenError(db_error) from db_error
        except NotFoundError as db_error:
            # Resource not found happens when a user tries to delete a
            # resource that does not exists
            raise ResourceNotFoundError(db_error) from db_error
        except IntegrityError as db_error:
            # Integrity errors happen mostly when the resource has
            # connections to other resources that should be deleted
            # first.
            raise ResourceIntegrityError(db_error) from db_error
        except Exception as db_error:
            # Every other error should result in a ServerError.
            raise ServerError(db_error) from db_error
        else:
            # If nothing went wrong, we create a object with the key
            # 'deleted' that we return to the client.
            return_response.data = {
                'deleted': True
            }

    # Return the created Response object
    return return_response
