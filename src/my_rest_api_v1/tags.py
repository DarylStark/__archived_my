"""
    Module that has the RESTAPIGroup for the 'tags' group of the API.
    This group can be used to get tag information.
"""
import re
from typing import Optional
from my_database.exceptions import MyDatabaseError
from my_database.tags import get_tags
from rest_api_generator import Authorization, Group, Response, ResponseType
from rest_api_generator.endpoint_scopes import EndpointScopes
from rest_api_generator.exceptions import ResourceNotFoundError

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
        REST API Endpoing '/tags/tags'. Returns a list with users.

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

        # Get the tags
        return_response.data = get_tags(
            auth.data.user,
            flt_id=tag_id
        )
    except MyDatabaseError:
        raise ResourceNotFoundError

    # Return the create RESTAPIResponse object
    return return_response
