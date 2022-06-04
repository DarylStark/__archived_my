""" Module that has the Group for the 'tags' group of the API.
    This group can be used to get tag information. """

import re
from typing import Optional
from flask import request
from my_database import validate_input
from my_database.date_tags import delete_date_tags, validation_fields
from my_database.exceptions import (FieldNotValidatedError, IntegrityError,
                                    MyDatabaseError, NotFoundError,
                                    PermissionDeniedError)
from my_database.date_tags import (create_date_tag, get_date_tags,
                                   delete_date_tags)
from rest_api_generator import Authorization, Group, Response, ResponseType
from rest_api_generator.endpoint_scopes import EndpointScopes
from rest_api_generator.exceptions import (InvalidInputError,
                                           ResourceForbiddenError,
                                           ResourceIntegrityError,
                                           ResourceNotFoundError,
                                           ServerError)

api_group_date_tags = Group(
    api_url_prefix='date_tags',
    name='date_tags',
    description='Contains endpoints for date tags'
)


@api_group_date_tags.register_endpoint(
    url_suffix=[
        r'date_tag'
    ],
    http_methods=['POST'],
    name='date_tag',
    description='Endpoint to create a date tag',
    auth_needed=True,
    auth_scopes=EndpointScopes(POST=['date_tags.create'])
)
def date_tags_create(auth: Optional[Authorization],
                     url_match: re.Match) -> Response:
    """
        REST API Endpoint '/date_tags/date_tag'. Creates a date tag.

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
    except (TypeError, FieldNotValidatedError) as e:
        raise InvalidInputError(e)

    # Create the tag
    try:
        new_object = create_date_tag(
            req_user=auth.data.user,
            **post_data
        )
    except IntegrityError as err:
        # Integrity errors happen mostly when the tag already
        # exists.
        raise ResourceIntegrityError(err)
    except Exception as err:
        # Every other error should result in a ServerError.
        raise ServerError(err)
    else:
        # If nothing went wrong, return the newly created object.
        return_response.data = new_object

    # Return the created Response object
    return return_response


@api_group_date_tags.register_endpoint(
    url_suffix=[
        r'date_tags',
        r'date_tags/',
        r'date_tags/(?P<resource_date>[0-9]{4}-[0-9]{2}-[0-9]{2})',
        r'date_tags/(?P<resource_id>[0-9]+)'
    ],
    http_methods=['GET'],
    name='date_tags',
    description='Endpoint to retrieve all or a subset of the date_tags',
    auth_needed=True,
    auth_scopes=EndpointScopes(GET=['date_tags.retrieve'])
)
def tags_retrieve(auth: Optional[Authorization],
                  url_match: re.Match) -> Response:
    """
        REST API Endpoint '/date_tags/date_tags'. Returns a list with date tags.

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
    except NotFoundError as err:
        # Resource not found happens when a user tries to get a
        # tag that does not exists
        raise ResourceNotFoundError(err)
    except Exception as err:
        # Every other error should result in a ServerError.
        raise ServerError(err)

    # Return the created Response object
    return return_response


@api_group_date_tags.register_endpoint(
    url_suffix=[
        r'date_tag/([0-9]+)'
    ],
    http_methods=['DELETE'],
    name='date_tag',
    description='Endpoint to delete a date tag',
    auth_needed=True,
    auth_scopes=EndpointScopes(
        DELETE=['date_tags.delete']
    )
)
def date_tags_delete(auth: Optional[Authorization],
                     url_match: re.Match) -> Response:
    """
        REST API Endpoint '/date_tags/date_tag/([0-9]+)'. Deletes a date tag.

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
    if request.method == 'DELETE':
        try:
            delete_date_tags(
                req_user=auth.data.user,
                date_tag_ids=resource_id
            )
        except PermissionDeniedError as err:
            # Permission denied errors happen when a user tries to
            # delete a type of resource he is not allowed to delete.
            raise ResourceForbiddenError(err)
        except NotFoundError as err:
            # Resource not found happens when a user tries to delete a
            # resource that does not exists
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

    # Return the created Response object
    return return_response
