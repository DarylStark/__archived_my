""" Module that has the Group for the 'api' group of the API.
    This group can be used to get specific API information. """
import re
from typing import Optional
from rest_api_generator import Authorization, Group, Response, ResponseType
from rest_api_generator.endpoint_scopes import EndpointScopes

api_group_api = Group(
    api_url_prefix='api',
    name='api',
    description='Contains endpoints for generic API requests'
)


@api_group_api.register_endpoint(
    url_suffix=['ping', 'ping/'],
    http_methods=['GET'],
    name='ping',
    description='Endpoint to check if the service is available',
    auth_needed=True,
    auth_scopes=EndpointScopes(GET=['api.ping'])
)
def ping(auth: Optional[Authorization],
         url_match: re.Match) -> Response:
    """
        REST API Endpoing '/api/ping'. Returns a 'pong' object which
        indicates that the REST API is running.

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

    # Set the data
    return_response.data = {
        'ping': 'pong'
    }

    # Return the create Response object
    return return_response
