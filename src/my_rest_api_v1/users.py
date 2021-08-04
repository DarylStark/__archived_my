"""
    Module that has the RESTAPIGroup for the 'users' group of the API.
    This group can be used to get user information.
"""
import re
from typing import Optional
from my_database.exceptions import MyDatabaseError
from my_database.users import get_users
from rest_api_generator import Authorization, Group, Response, ResponseType
from rest_api_generator.endpoint_scopes import EndpointScopes
from rest_api_generator.exceptions import ResourceNotFoundError

api_group_users = Group(
    api_url_prefix='users',
    name='users',
    description='Contains endpoints for users'
)


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
        user_id = None
        if len(url_match.groups()) > 0:
            user_id = int(url_match.groups(0)[0])
            return_response.type = ResponseType.SINGLE_RESOURCE

        # Get the users
        return_response.data = get_users(
            auth.data.user,
            flt_id=user_id
        )

        if len(return_response.data) == 0 and user_id is not None:
            raise ResourceNotFoundError('Not a valid user ID')

        # If the user requested only one resource, we only put that
        # resource in the return
        if user_id is not None:
            return_response.data = return_response.data[0]
    except MyDatabaseError:
        raise ResourceNotFoundError

    # Return the create RESTAPIResponse object
    return return_response
