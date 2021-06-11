"""
    Module that has the RESTAPIGroup for the 'api' group of the API.
    This group can be used to get specific API information.
"""
# ---------------------------------------------------------------------
# Imports
import re
from typing import Optional
from rest_api_generator import RESTAPIGroup, RESTAPIResponse, ResponseType
from rest_api_generator import RESTAPIAuthorization
from rest_api_generator.rest_api_endpoint_scopes import RESTAPIEndpointScopes
# ---------------------------------------------------------------------
# API group
api_group_api = RESTAPIGroup(
    api_url_prefix='api',
    name='api',
    description='Contains endpoints for generic API requests'
)
# ---------------------------------------------------------------------
# Endpoints


@api_group_api.register_endpoint(
    url_suffix=['ping', 'ping/'],
    http_methods=['GET'],
    name='ping',
    description='Endpoint to check if the service is available',
    auth_needed=True,
    auth_scopes=RESTAPIEndpointScopes(GET=['api.ping'])
)
def ping(auth: Optional[RESTAPIAuthorization],
         url_match: re.Match) -> RESTAPIResponse:
    """
        REST API Endpoing '/api/ping'. Returns a 'pong' object which
        indicates that the REST API is running.

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
    return_response = RESTAPIResponse(ResponseType.SINGLE_RESOURCE)

    # Set the data
    return_response.data = {
        'ping': 'pong'
    }

    # Return the create RESTAPIResponse object
    return return_response
# ---------------------------------------------------------------------