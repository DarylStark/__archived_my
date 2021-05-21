"""
    This module includes the RESTAPIGenerator class that can be used to
    generate the REST API blueprint.
"""
# ---------------------------------------------------------------------
# Imports
from flask import Blueprint
from typing import Callable, List, Optional, Set
from rest_api_generator.exceptions import InvalidGroupError
from rest_api_generator.rest_api_endpoint_url import RESTAPIEndpointURL
from rest_api_generator.rest_api_group import RESTAPIGroup
# ---------------------------------------------------------------------


class RESTAPIGenerator:
    """ Class that can be used to generate APIs """

    def __init__(self,
                 bp_name: str = 'api_generator',
                 bp_import_name: str = __name__,
                 bp_url_prefix: Optional[str] = None) -> None:
        """ The initiator can be used to configure the Flask Blueprint
        """

        # Create a empty set with registered groups. The user can add
        # groups with the 'register_group' command. We make this a set
        # to make sure no groups are added more then once.
        self.groups: Set[RESTAPIGroup] = set()

        # Create a Flask Blueprint. This can be used to connect the
        # REST API to a existing Flask app
        self.blueprint: Blueprint = Blueprint(
            bp_name, bp_import_name, url_prefix=bp_url_prefix)

        # Create a list with acceptable HTTP methods. By default, we
        # only accept 'GET' requests, but the user can add methods to
        # accept with the 'add_method' method.
        self.accepted_http_methods = [
            'GET'
        ]

        # Set default values for the authorization options
        self.use_authorization: bool = False
        self.authorization_function: Optional[Callable[[str, List[str]], bool]]

        # Register the routes
        self.add_routes()

    def add_method(self, method: str) -> None:
        """ Method to add HTTP methods to the accepted list """
        self.accepted_http_methods.append(method)

    def remove_method(self, method: str) -> None:
        """ Method to remove HTTP methods from the accepted list """
        try:
            self.accepted_http_methods.remove(method)
        except ValueError:
            # If the item wasn't in the list, we get an ValueError
            # exception. We don't do anything in that case.
            pass

    def add_routes(self) -> None:
        """ Method to register the routes for the Blueprint """

        # We create a callback method for the Blueprint and make sure
        # the Flask routing redirects every request to this method.
        @ self.blueprint.route('/', defaults={'path': ''},
                               methods=self.accepted_http_methods)
        @ self.blueprint.route('/<path:path>',
                               methods=self.accepted_http_methods)
        def execute_url(path: str) -> str:
            url_list: List[RESTAPIEndpointURL] = self.get_all_endpoints()
            for endpoint in url_list:
                if endpoint.url == path:
                    if self.authorization_function \
                            and endpoint.endpoint.auth_needed:
                        if endpoint.endpoint.auth_permissions.GET:
                            if self.authorization_function(
                                'my_api_key',
                                endpoint.endpoint.auth_permissions.GET
                            ):
                                return f'Auth: {endpoint.endpoint.func()}'
                            else:
                                return 'Not authorized'

                    return endpoint.endpoint.func()

            # No matching URL found
            return '404: Page not found'

    def register_group(self, group: RESTAPIGroup) -> None:
        """ Method to register a group for the REST API """

        # Check if the group is of the correct type. If it isn't, the
        # user made a mistake and we raise an exception
        if isinstance(group, RESTAPIGroup):
            # Add the group to the set
            self.groups.add(group)
        else:
            # Wrong type, give error
            raise InvalidGroupError(
                f'Group is of type "{type(group)}", expected "{RESTAPIGroup}"')

    def register_authorization_method(self,
                                      func: Callable[[str, List[str]], bool]
                                      ) -> None:
        """ Method to set a authorization method for the REST API.
            Should be used as a decorator

            Parameter
            ---------
            func : Callable[[str, str], bool]
                Function that takes in two strings (one for the
                authorization data and one for the requested
                permission). Should return True if the request is
                authorized and False if the request is not authorized

            Returns
            -------
            None
        """
        self.authorization_function = func

    def get_all_endpoints(self) -> List[RESTAPIEndpointURL]:
        """ Method that returns all RESTAPIEndpoints for this REST API
            in a list with RESTAPIEndpointURL objects

            Parameter
            ---------
            None

            Returns
            -------
            list[RESTAPIEndpointURL]
                A list with RESTAPIEndpointURLs for this REST API
        """

        # Create a empty list that we can return later on
        return_list: List[RESTAPIEndpointURL] = list()

        # Add endpoints from groups.
        for group in self.groups:
            return_list += group.get_endpoints()

        # Return the list
        return return_list
# ---------------------------------------------------------------------
