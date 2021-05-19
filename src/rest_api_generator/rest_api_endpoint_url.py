"""
    This module includes the RESTAPIEndpointURL which is a object that
    contains the URL for and endpoint and RESTAPIEndpoint object.
"""
# ---------------------------------------------------------------------
# Imports
from rest_api_generator.rest_api_endpoint import RESTAPIEndpoint
# ---------------------------------------------------------------------


class RESTAPIEndpointURL:
    """ Class used to create objects that contain a URL as string and
        a RESTAPIEndpoint object """

    def __init__(self, url: str, endpoint: RESTAPIEndpoint):
        """ The initiator sets the URL and the endpoint

            Parameters
            ----------
            url : str
                The url that belongs to this RESTAPIEndpoint

            endpoint : RESTAPIEndpoint
                The RESTAPIEndpoint object for this URL
        """
        self.url = url
        self.endpoint = endpoint
# ---------------------------------------------------------------------
