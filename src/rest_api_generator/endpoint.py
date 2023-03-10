""" This module includes the Endpoint which represents a API endpoint.
"""

import re
from dataclasses import dataclass, field
from typing import Callable, List, Optional

from rest_api_generator.authorization import Authorization
from rest_api_generator.endpoint_scopes import EndpointScopes
from rest_api_generator.response import Response


@dataclass
class Endpoint:
    """ Class that represent a API endpoint

        Members
        -------
        url_suffix : str
            The URL suffix for the endpoint.

        func : Callable[[], Response]
            The function to run for this endpoint.

        http_methods : List[str] [default=list()]
            HTTP methods that this API endpoint supports.

        name : str [default='']
            The name for the API endpoint. Is used in help pages.

        description : str [default='']
            Description for the API endpoint. Is used in help pages.

        auth_needed : bool [default=bool]
            Determines if there is authorization needed for this
            endpoint.

        auth_scopes : Optional[EndpointScope] [default=None]
            A list of permissions which the user needs at least one of
            to authorize for this endpoint.
    """

    # Mandatory members
    url_suffix: List[str]
    func: Callable[[
        Optional[Authorization],
        Optional[re.Match]
    ], Response]
    http_methods: List[str] = field(default_factory=list)

    # Members for help pages
    name: Optional[str] = ''
    description: Optional[str] = ''

    # Members for authentication
    auth_needed: Optional[bool] = False
    auth_scopes: Optional[EndpointScopes] = None
