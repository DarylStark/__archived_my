""" Module that has the Group for the 'dashboard' group of the API.
    This group can be used to get and update dashboard information. """

import re
from typing import Optional

from flask import request

from my_database import validate_input
from my_database.date_tags import (create_date_tag, delete_date_tags,
                                   get_date_tags, validation_fields)
from my_database.exceptions import (FieldNotValidatedError, IntegrityError,
                                    NotFoundError, PermissionDeniedError)
from rest_api_generator import Authorization, Group, Response, ResponseType
from rest_api_generator.endpoint_scopes import EndpointScopes
from rest_api_generator.exceptions import (InvalidInputError,
                                           ResourceForbiddenError,
                                           ResourceIntegrityError,
                                           ResourceNotFoundError, ServerError)

api_group_dashboard = Group(
    api_url_prefix='dashboard',
    name='dashboard',
    description='Contains endpoints for the dashboard'
)


@api_group_dashboard.register_endpoint(
    url_suffix=[
        r'tag'
    ],
    http_methods=['POST'],
    name='tag_create',
    description='Endpoint to tag a specific date',
    auth_needed=True,
    auth_scopes=EndpointScopes(POST=['date_tags.create'])
)
def tag(auth: Optional[Authorization],
        url_match: re.Match) -> Response:
    """
        REST API Endpoint '/dashboard/tag'. Tags a specific date.

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

    # Set the needed fields
    required_fields = {
        'date': validation_fields['date'],
        'tag_id': validation_fields['tag_id']
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

    # Create the tag
    try:
        new_object = create_date_tag(
            req_user=auth.data.user,
            **post_data
        )
    except IntegrityError as db_error:
        # Integrity errors happen mostly when the tag already
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


@api_group_dashboard.register_endpoint(
    url_suffix=[
        r'tags',
        r'tags/',
        r'tags/(?P<resource_date>[0-9]{4}-[0-9]{2}-[0-9]{2})',
        r'tags/(?P<resource_id>[0-9]+)'
    ],
    http_methods=['GET'],
    name='tags_retrieve',
    description='Endpoint to retrieve all or a subset of the tags for a specific date',
    auth_needed=True,
    auth_scopes=EndpointScopes(GET=['date_tags.retrieve'])
)
def date_tags_retrieve(auth: Optional[Authorization],
                       url_match: re.Match) -> Response:
    """
        REST API Endpoint '/dashboard/tags'. Returns a list with date tags.

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
            'flt_date': None
        }

        # Check if we received a ID
        if 'resource_id' in url_match.groupdict().keys():
            filters['flt_id'] = int(url_match.group('resource_id'))
            return_response.type = ResponseType.SINGLE_RESOURCE

        # Check if we received a title
        if 'resource_date' in url_match.groupdict().keys():
            resource_date = url_match.group('resource_date')
            filters['flt_date'] = resource_date

        # Get the resources
        return_response.data = get_date_tags(
            auth.data.user,
            **filters
        )
    except NotFoundError as error:
        # Resource not found happens when a user tries to get a
        # tag that does not exists
        raise ResourceNotFoundError(error)
    except Exception as db_error:
        # Every other error should result in a ServerError.
        raise ServerError(db_error) from db_error

    # Return the created Response object
    return return_response


@api_group_dashboard.register_endpoint(
    url_suffix=[
        r'tag/([0-9]+)'
    ],
    http_methods=['DELETE'],
    name='tag_delete',
    description='Endpoint to delete a tag from a specific date',
    auth_needed=True,
    auth_scopes=EndpointScopes(
        DELETE=['date_tags.delete']
    )
)
def date_tags_delete(auth: Optional[Authorization],
                     url_match: re.Match) -> Response:
    """
        REST API Endpoint '/dashboard/date_tag/([0-9]+)'. Deletes a date tag.

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

    # Get the tag ID
    resource_id = int(url_match.groups(0)[0])

    # Delete tag
    try:
        delete_date_tags(
            req_user=auth.data.user,
            date_tag_ids=resource_id
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
