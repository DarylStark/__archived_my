"""
    This module includes the RESTAPIGroup which represents a API group.
"""
# ---------------------------------------------------------------------
# Imports
from logging import getLogger
import re
from typing import Callable, List, Optional
from rest_api_generator.rest_api_authorization import RESTAPIAuthorization
from rest_api_generator.rest_api_endpoint_scopes\
    import RESTAPIEndpointScopes
from rest_api_generator.rest_api_endpoint import RESTAPIEndpoint
from rest_api_generator.rest_api_endpoint_url import RESTAPIEndpointURL
from rest_api_generator.rest_api_response import RESTAPIResponse
# ---------------------------------------------------------------------


class RESTAPIGroup:
    """ Class that represent a API group """

    def __init__(self,
                 api_url_prefix: str,
                 name: Optional[str] = None,
                 description: Optional[str] = None) -> None:
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

        # Set a logger for this object
        self.logger = getLogger(f'API_Group_{api_url_prefix}')
        self.logger.debug('Created')

        # Set the class variables for the given arguments
        self.url_prefix: str = api_url_prefix
        self.name: Optional[str] = api_url_prefix
        self.description: Optional[str] = description

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
        """ Method to add a subgroup to this group.

            Parameters
            ----------
            group : RESTAPIGroup
                The group object to add

            Returns
            -------
            None
        """
        self.logger.debug(f'Adding subgroup: {group.name}')
        self.subgroups.append(group)

    def register_endpoint(
            self,
            url_suffix: List[str],
            http_methods: List[str] = None,
            name: str = None,
            description: str = None,
            auth_needed: bool = False,
            auth_scopes:
            Optional[RESTAPIEndpointScopes] = None) -> Callable:
        """ Decorator to register a endpoint for this REST API group

            Parameters
            ----------
            url_suffix : str
                The URL suffix for the endpoint.

            name : str (default=None)
                The name for the API endpoint. Is used in help pages.

            http_methods : Optional[RESTAPIEndpointPermissions]
                RESTAPIEndpointPermissions object that specifies the
                needed OAuth permissions for this endpoint.

            description : str (default=None)
                Description for the API endpoint. Is used in help
                pages.

            auth_needed : bool (default=False)
                Specifies if authorization is required for this
                endpoint.

            auth_scpoes : Optional[RESTAPIEndpointPermissions]
                          (default=None)
                Specifies the scopes for this endpoint. In the
                registered auth method, the user can use this
                information to authorize a request.

            Returns
            -------
            method
                The decorator
        """

        def decorator(func: Callable[[
            Optional[RESTAPIAuthorization],
            Optional[re.Match]
        ], RESTAPIResponse]) -> Callable[[
            Optional[RESTAPIAuthorization],
            Optional[re.Match]
        ], RESTAPIResponse]:
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
            endpoint: RESTAPIEndpoint = RESTAPIEndpoint(
                url_suffix=url_suffix,
                func=func,
                http_methods=http_methods,
                name=name,
                description=description,
                auth_needed=auth_needed,
                auth_scopes=auth_scopes
            )
            self.endpoints.append(endpoint)

            self.logger.debug(f'Registered endpoint: {endpoint.name}')

            # Return the function so it can still be used
            return func

        # Return the decorator
        return decorator

    def get_endpoints(self) -> List[RESTAPIEndpointURL]:
        """ Method that returns a list with RESTAPIEndpointURL objects.
            These objects contain the URL and RESTAPIEndpoint objects
            for all registered endpoints in this group and subgroup.

            Parameter
            ---------
            None

            Returns
            -------
            list[RESTAPIEndpointURL]
                A list with RESTAPIEndpointURLs for this group and it's
                subgroups
        """

        self.logger.debug('Creating list of endpoint URLs')

        # Create a empty list that we can fill to return
        return_list: List[RESTAPIEndpointURL] = list()

        # Add local endpoints
        for endpoint in self.endpoints:
            # Loop through all suffixes for this endpoint
            for suffixes in endpoint.url_suffix:
                # Create a object
                endpoint_url = RESTAPIEndpointURL(
                    url=f'{self.url_prefix}{suffixes}',
                    endpoint=endpoint
                )

                # Add it to the list
                return_list.append(endpoint_url)

        # Add endpoints from subgroups. We prepend the URL prefix for
        # this group to it so we get a full URL
        for group in self.subgroups:
            # Get the endpoints and prepend the local prefix
            endpoint_list: List[RESTAPIEndpointURL] = group.get_endpoints()
            for endpoint in endpoint_list:
                endpoint.url = f'{self.url_prefix}{endpoint.url}'

            # Add the endpoints to the return list
            return_list += endpoint_list

        self.logger.debug('Created list')

        # Return the list
        return return_list
# ---------------------------------------------------------------------
