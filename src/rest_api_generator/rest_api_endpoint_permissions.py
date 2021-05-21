"""
    This module includes the RESTAPIEndpointPermissions class which is
    a object that contains the permissions for a specific
    RESTAPIEndpoint
"""
# ---------------------------------------------------------------------
# Imports
from dataclasses import dataclass
from typing import List, Optional
# ---------------------------------------------------------------------


@dataclass
class RESTAPIEndpointPermissions:
    """ Class used to create objects that contain the permissions for a
        specific RESTAPIEndpoint

        Members
        -------
        GET : str
            The permissions for a GET request

        POST : str
            The permissions for a POST request

        PUT : str
            The permissions for a PUT request

        DELETE : str
            The permissions for a DELETE request
    """

    GET: Optional[List[str]] = None
    POST: Optional[List[str]] = None
    PUT: Optional[List[str]] = None
    DELETE: Optional[List[str]] = None
# ---------------------------------------------------------------------
