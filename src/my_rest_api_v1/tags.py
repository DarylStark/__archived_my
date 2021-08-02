"""
    Module that has the RESTAPIGroup for the 'tags' group of the API.
    This group can be used to get tag information.
"""
import re
from typing import Optional
from flask import request
from my_database.exceptions import MyDatabaseError, IntegrityError
from my_database.generic import add_object
from my_database.tags import get_tags
from my_database_model import user
from my_database_model.tag import Tag
from rest_api_generator import Authorization, Group, Response, ResponseType
from rest_api_generator.endpoint_scopes import EndpointScopes
from rest_api_generator.exceptions import (ResourceForbiddenError, ResourceIntegrityError,
                                           ResourceNotFoundError)

api_group_tags = Group(
    api_url_prefix='tags',
    name='tags',
    description='Contains endpoints for tags'
)


@api_group_tags.register_endpoint(
    url_suffix=['tags', 'tags/', 'tags/([0-9]+)'],
    http_methods=['GET'],
    name='tags',
    description='Endpoint to retrieve all or a subset of the tags',
    auth_needed=True,
    auth_scopes=EndpointScopes(GET=['tags.retrieve'])
)
def tags(auth: Optional[Authorization],
         url_match: re.Match) -> Response:
    """
        REST API Endpoing '/tags/tags'. Returns a list with tags.

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
        tag_id = None
        if len(url_match.groups()) > 0:
            tag_id = int(url_match.groups(0)[0])
            return_response.type = ResponseType.SINGLE_RESOURCE

        # Get the tags
        return_response.data = get_tags(
            auth.data.user,
            flt_id=tag_id
        )

        if len(return_response.data) == 0 and tag_id is not None:
            raise ResourceNotFoundError('Not a valid tag ID')
    except MyDatabaseError:
        raise ResourceNotFoundError

    # Return the create RESTAPIResponse object
    return return_response


@api_group_tags.register_endpoint(
    url_suffix=['tag'],
    http_methods=['POST'],
    name='tag',
    description='Endpoint to create a tag',
    auth_needed=True,
    auth_scopes=EndpointScopes(POST=['tags.create'])
)
def tag(auth: Optional[Authorization],
        url_match: re.Match) -> Response:
    """
        REST API Endpoing '/tags/tag'. Creates a tag.

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
        needed_fields = ['title']
        for field in needed_fields:
            if field not in post_data.keys():
                raise ResourceNotFoundError(
                    f'Field "{field}" missing in request')

        # Create a tag
        new_object = Tag(
            user_id=auth.data.user_id,
            title=post_data['title']
        )

        # Add the object
        try:
            add_object(new_object)
        except IntegrityError:
            raise ResourceIntegrityError('Tag already exists')
        else:
            return_response.data = new_object

    except MyDatabaseError:
        raise ResourceNotFoundError

    # Return the create RESTAPIResponse object
    return return_response
