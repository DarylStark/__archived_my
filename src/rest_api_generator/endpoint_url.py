"""
    This module includes the RESTAPIEndpointURL which is a object that
    contains the URL for and endpoint and RESTAPIEndpoint object.
"""
# ---------------------------------------------------------------------
# Imports
from rest_api_generator.endpoint import RESTAPIEndpoint
from dataclasses import dataclass
# ---------------------------------------------------------------------


@dataclass
class RESTAPIEndpointURL:
    """ Class used to create objects that contain a URL as string and
        a RESTAPIEndpoint object.

        Members
        -------
        url : str
            The URL for the endpoint

        endpoint : RESTAPIEndpoint
            The endpoint object for the endpoint
    """

    url: str
    endpoint: RESTAPIEndpoint
# ---------------------------------------------------------------------
