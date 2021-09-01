""" This module includes the EndpointURL which is a object that
    contains the URL for and endpoint and Endpoint object. """
from dataclasses import dataclass
from rest_api_generator.endpoint import Endpoint


@dataclass
class EndpointURL:
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
    endpoint: Endpoint
