"""
    This module includes the EndpointScopes class which is a object
    that contains the auth scopes for a specific Endpoint
"""
# ---------------------------------------------------------------------
# Imports
from dataclasses import dataclass
from typing import List, Optional
# ---------------------------------------------------------------------


@dataclass
class EndpointScopes:
    """ Class used to create objects that contain the auth scopes for a
        specific RESTAPIEndpoint

        Members
        -------
        POST : List[str]
            The permissions for a POST request

        GET : List[str]
            The permissions for a GET request

        PUT : List[str]
            The permissions for a PUT request

        PATCH : List[str]
            The permissions for a PATCH request

        DELETE : List[str]
            The permissions for a DELETE request
    """

    POST: Optional[List[str]] = None
    GET: Optional[List[str]] = None
    PUT: Optional[List[str]] = None
    PATCH: Optional[List[str]] = None
    DELETE: Optional[List[str]] = None
# ---------------------------------------------------------------------
