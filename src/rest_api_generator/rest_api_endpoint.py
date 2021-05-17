"""
    This module includes the RESTAPIEndpoint which represents a API
    endpoint.
"""
# ---------------------------------------------------------------------
from typing import List
# ---------------------------------------------------------------------


class RESTAPIEndpoint:
    """ Class that represent a API endpoint """

    def __init__(self,
                 url_suffix: str,
                 func,
                 name: str = None,
                 description: str = None,
                 http_methods: List[str] = None):
        """ Inititator sets default values for the endpoint.

            Parameters
            ----------
            url_suffix : str
                The URL suffix for the endpoint.

            func : 
                The method/function to run for this endpoint

            name : str (default=None)
                The name for the API endpoint. Is used in help pages

            description : str (default=None)
                Description for the API endpoint. Is used in help pages

            http_methods : List[str] (default=None)
                HTTP methods that this API endpoint supports

            Returns
            -------
            method
                The decorator
        """
        pass
# ---------------------------------------------------------------------
