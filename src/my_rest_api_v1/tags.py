""" Module that has the Group for the 'tags' group of the API.
    This group can be used to get tag information. """

import re
from typing import Optional
from flask import request
from my_database import validate_input
from my_database.tags import validation_fields
from my_database.exceptions import (FieldNotValidatedError, IntegrityError,
                                    MyDatabaseError, NotFoundError,
                                    PermissionDeniedError)
from my_database.tags import create_tag, delete_tag, get_tags, update_tag
from rest_api_generator import Authorization, Group, Response, ResponseType
from rest_api_generator.endpoint_scopes import EndpointScopes
from rest_api_generator.exceptions import (InvalidInputError,
                                           ResourceForbiddenError,
                                           ResourceIntegrityError,
                                           ResourceNotFoundError,
                                           ServerError)

api_group_tags = Group(
    api_url_prefix='tags',
    name='tags',
    description='Contains endpoints for tags'
)


@api_group_tags.register_endpoint(
    url_suffix=['tag'],
    http_methods=['POST'],
    name='tag',
    description='Endpoint to create a tag',
    auth_needed=True,
    auth_scopes=EndpointScopes(POST=['tags.create'])
)
def tags_create(auth: Optional[Authorization],
                url_match: re.Match) -> Response:
    """
        REST API Endpoint '/tags/tag'. Creates a tag.

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
        'title': validation_fields['title']
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
        new_object = create_tag(
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


@api_group_tags.register_endpoint(
    url_suffix=[
        'tags',
        'tags/',
        'tags/(?P<resource_id>[0-9]+)',
        'tags/(?P<resource_title>[A-Za-z][A-Za-z0-9\-_.\+]+)'
    ],
    http_methods=['GET'],
    name='tags',
    description='Endpoint to retrieve all or a subset of the tags',
    auth_needed=True,
    auth_scopes=EndpointScopes(GET=['tags.retrieve'])
)
def tags_retrieve(auth: Optional[Authorization],
                  url_match: re.Match) -> Response:
    """
        REST API Endpoint '/tags/tags'. Returns a list with tags.

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
            'flt_title': None
        }

        # Check if we received a ID
        if 'resource_id' in url_match.groupdict().keys():
            filters['flt_id'] = int(url_match.group('resource_id'))
            return_response.type = ResponseType.SINGLE_RESOURCE

        # Check if we received a title
        if 'resource_title' in url_match.groupdict().keys():
            # Replace plus signes with a spaces, so a user can retrieve
            # tags like 'my tag' as 'my+tag'
            resource_title = url_match.group('resource_title')
            resource_title = resource_title.replace('+', ' ')
            filters['flt_title'] = resource_title
            return_response.type = ResponseType.SINGLE_RESOURCE

        # Get the resources
        return_response.data = get_tags(
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


@api_group_tags.register_endpoint(
    url_suffix=['tag/([0-9]+)'],
    http_methods=['PATCH', 'DELETE'],
    name='tag',
    description='Endpoint to edit or delete a tag',
    auth_needed=True,
    auth_scopes=EndpointScopes(
        PATCH=['tags.update'],
        DELETE=['tags.delete']
    )
)
def tags_update_delete(auth: Optional[Authorization],
                       url_match: re.Match) -> Response:
    """
        REST API Endpoint '/tags/tag/([0-9]+)'. Edits or deletes a tag.

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

    # Update tag
    if request.method == 'PATCH':
        # Get the data
        post_data = request.json

        # Set the needed fields
        required_fields = {
            'title': validation_fields['title']
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

        # Update the tag
        try:
            changed_resource = update_tag(
                req_user=auth.data.user,
                tag_id=resource_id,
                **post_data
            )
        except NotFoundError as err:
            # Resource not found happens when a user tries to change a
            # tag that does not exists
            raise ResourceNotFoundError(err)
        except IntegrityError as err:
            # Integrity errors happen mostly when the tag already
            # exists.
            raise ResourceIntegrityError(err)
        except Exception as err:
            # Every other error should result in a ServerError.
            raise ServerError(err)

        # If nothing went wrong, return the newly created object.
        return_response.data = changed_resource

    # Delete tag
    if request.method == 'DELETE':
        try:
            delete_tag(
                req_user=auth.data.user,
                tag_id=resource_id
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
