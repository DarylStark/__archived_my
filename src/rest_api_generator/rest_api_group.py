"""
    This module includes the RESTAPIGroup which represents a API group.
"""
# ---------------------------------------------------------------------
# Imports
from typing import List
from rest_api_generator.rest_api_endpoint import RESTAPIEndpoint
# ---------------------------------------------------------------------


class RESTAPIGroup:
    """ Class that represent a API group """

    def __init__(self,
                 api_url_prefix: str,
                 name: str = None,
                 description: str = None) -> None:
        """ The initiator sets a empty list of endpoint and initializes
            the API group.

            Parameters
            ----------
            api_url_prefix : str
                The URL prefix for the API group. If the URL prefix for
                the API 'api' is, and the URL prefix for this group is
                'users', the complete URL for this group will be
                '/api/users'.

            name : str (default=None)
                The name for the API group. Is used in help pages

            description : str (default=None)
                Description for the API group. Is used in help pages

            Returns
            -------
            None
        """

        # Set the class variables for the given arguments
        self.url_prefix = api_url_prefix
        self.name = api_url_prefix
        self.description = description

        # If the user didn't add a trailing slash to the URL prefix, we
        # add it manually
        if self.url_prefix[-1] != '/':
            self.url_prefix += '/'

        # If name is given, we can set it
        if name:
            self.name = name

        # Create a empty list of endpoint
        self.endpoints: List[RESTAPIEndpoint] = list()

        # Create a empty list of subgroups
        self.subgroups: List[RESTAPIGroup] = list()

    def add_subgroup(self, group: 'RESTAPIGroup') -> None:
        """ Method to add a subgroup to this group

            Parameters
            ----------
            group : RESTAPIGroup
                The group object to add

            Returns
            -------
            None        
        """
        self.subgroups.append(group)

    def register_endpoint(self,
                          url_suffix: str,
                          name: str = None,
                          description: str = None,
                          http_methods: List[str] = None):
        """ Decorator to register a endpoint for this REST API group

            Parameters
            ----------
            url_suffix : str
                The URL suffix for the endpoint.

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

        def decorator(func):
            """ The decorator registers the API endpoint

                Parameters
                ----------
                func
                    The function to register

                Returns
                -------
                func
                    The function that is given
            """
            # Add the endpoint to the list
            endpoint = RESTAPIEndpoint(
                url_suffix=url_suffix,
                func=func,
                name=name,
                description=description,
                http_methods=http_methods
            )
            self.endpoints.append(endpoint)

            # Return the function so it can still be used
            return func

        # Return the decorator
        return decorator
# ---------------------------------------------------------------------
