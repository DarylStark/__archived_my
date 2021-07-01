"""
    Module that has the RESTAPIGroup for the 'users' group of the API.
    This group can be used to get user information.
"""
# ---------------------------------------------------------------------
# Imports
import re
from typing import Optional
from my_database.exceptions import MyDatabaseError
from rest_api_generator import RESTAPIGroup, RESTAPIResponse, ResponseType
from rest_api_generator import RESTAPIAuthorization
from rest_api_generator.exceptions import ResourceNotFoundError
from rest_api_generator.rest_api_endpoint_scopes import RESTAPIEndpointScopes
from my_database.users import get_users
# ---------------------------------------------------------------------
# API group
api_group_users = RESTAPIGroup(
    api_url_prefix='users',
    name='users',
    description='Contains endpoints for users'
)
# ---------------------------------------------------------------------
# Endpoints


@api_group_users.register_endpoint(
    url_suffix=['users', 'users/'],
    http_methods=['GET'],
    name='users',
    description='Endpoint to retrieve all or a subset of the users',
    auth_needed=True,
    auth_scopes=RESTAPIEndpointScopes(GET=['users.retrieve'])
)
def users(auth: Optional[RESTAPIAuthorization],
          url_match: re.Match) -> RESTAPIResponse:
    """
        REST API Endpoing '/users/users'. Returns a list with users.

        Parameters
        ----------
        auth : RESTAPIAuthorization
            A object that contains authorization information. Because
            this endpoint doesn't expect authorization, this has to be
            empty at all times.

        url_match : re.Match
            Endpoint that contains the regex match object that was used
            to match the URL.

        Returns
        -------
        RESTAPIResponse
            The API response
    """

    # Create a RESTAPIResponse object
    return_response = RESTAPIResponse(ResponseType.RESOURCE_SET)

    # Set the data
    try:
        return_response.data = get_users(auth.data.user)
    except MyDatabaseError:
        raise ResourceNotFoundError

    # Return the create RESTAPIResponse object
    return return_response
# ---------------------------------------------------------------------
