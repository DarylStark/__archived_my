"""
    This module includes the RESTAPIEndpoint which represents a API
    endpoint.
"""
# ---------------------------------------------------------------------
import re
from typing import Callable, List, Optional
from dataclasses import dataclass, field
from rest_api_generator.rest_api_authorization import RESTAPIAuthorization
from rest_api_generator.rest_api_endpoint_permissions\
    import RESTAPIEndpointPermissions
from rest_api_generator.rest_api_response import RESTAPIResponse
# ---------------------------------------------------------------------


@dataclass
class RESTAPIEndpoint:
    """ Class that represent a API endpoint

        Members
        -------
        url_suffix : str
            The URL suffix for the endpoint.

        func : Callable[[], RESTAPIResponse]
            The function to run for this endpoint.

        http_methods : List[str](default=None)
            HTTP methods that this API endpoint supports.

        name : str(default=None)
            The name for the API endpoint. Is used in help pages.

        description : str(default=None)
            Description for the API endpoint. Is used in help pages.

        auth_needed : bool
            Determines if there is authorization needed for this
            endpoint.

        auth_permissions : List[str]
            A list of permissions which the user needs at least one of
            to authorize for this endpoint.
    """

    # Mandatory members
    url_suffix: List[str]
    func: Callable[[
        Optional[RESTAPIAuthorization],
        Optional[re.Match]
    ], RESTAPIResponse]
    http_methods: List[str] = field(default_factory=list)

    # Members for help pages
    name: Optional[str] = ''
    description: Optional[str] = ''

    # Members for authentication
    auth_needed: Optional[bool] = False
    auth_scopes: Optional[RESTAPIEndpointPermissions] = None
# ---------------------------------------------------------------------
