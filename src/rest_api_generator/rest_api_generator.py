"""
    This module includes the RESTAPIGenerator class that can be used to
    generate the REST API blueprint.
"""
# ---------------------------------------------------------------------
# Imports
import re
from flask import Blueprint, request, Response, abort
from typing import Callable, List, Optional, Set, Union
from rest_api_generator.exceptions import InvalidGroupError, \
    UnauthorizedForResourceError, ResourceForbiddenError, ResourceNotFoundError
from rest_api_generator.rest_api_endpoint_url import RESTAPIEndpointURL
from rest_api_generator.rest_api_group import RESTAPIGroup
from rest_api_generator.rest_api_authorization import RESTAPIAuthorization
from rest_api_generator.rest_api_json_encoder import RESTAPIJSONEncoder
from rest_api_generator.rest_api_response import RESTAPIResponse, ResponseType
from json import dumps
from math import ceil
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
        self.authorization_function: Optional[Callable[[
            str, Optional[List[str]]], RESTAPIAuthorization]]

        # Set defaults for API results
        self.default_limit: int = 25
        self.default_pretty: bool = False

        # Register the routes
        self.add_routes()

    def accept_method(self, method: str) -> None:
        """ Method to add HTTP methods to the accepted list """
        self.accepted_http_methods.append(method)

    def deny_method(self, method: str) -> None:
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
        @self.blueprint.route('/', defaults={'path': ''},
                              methods=self.accepted_http_methods)
        @self.blueprint.route('/<path:path>',
                              methods=self.accepted_http_methods)
        def execute_url(path: str) -> Union[str, Response]:
            """ Method that gets run as soon as a REST API Endpoint
                gets requested.

                Parameter
                ---------
                path : str
                    The path the user requested

                Returns
                -------
                str
                    The requested API end result
            """
            # Get a list of all endpoints registered in this REST API
            url_list: List[RESTAPIEndpointURL] = self.get_all_endpoints()

            # Filter the list to only include the URL that we need
            filtered_url_list = [
                (endpoint, re.fullmatch(endpoint.url, path))
                for endpoint in url_list
                if re.fullmatch(endpoint.url, path)
            ]

            # Loop through the endpoints and fine one that matches the
            # requested url
            if len(filtered_url_list) == 1:
                # Found the requested endpoint. Retrieve the endpoint
                # object from it
                endpoint = filtered_url_list[0][0].endpoint

                # First we check if the HTTP method is valid for this
                # endpoint
                if request.method in endpoint.http_methods:
                    # Set empty auth variable
                    auth: Optional[RESTAPIAuthorization] = None

                    # Method is allowed, check if permissions are
                    # needed
                    if endpoint.auth_needed and self.authorization_function:
                        # Permissions needed, get if the user is
                        # authorized to run this endpoint
                        try:
                            # Check if the user is authorized
                            auth = \
                                self.authorization_function(
                                    request.headers['Authorization'],
                                    endpoint.auth_permissions.__getattribute__(
                                        request.method)
                                )
                        except (AttributeError, KeyError):
                            auth = RESTAPIAuthorization(authorized=False)

                        # Check the given value. If the user is not
                        # authorized, we raise a 403 error
                        if not auth.authorized:
                            abort(403)

                    # Get the variables given in the URL (if any are
                    # given).
                    page: int = 1
                    limit: int = self.default_limit
                    pretty: bool = self.default_pretty

                    if 'page' in request.args.keys():
                        page = int(request.args['page'])
                    if 'limit' in request.args.keys():
                        limit = int(request.args['limit'])
                    if 'pretty' in request.args.keys():
                        pretty = True

                    # Done! Run the endpoint method
                    try:
                        return_value: RESTAPIResponse = endpoint.func(
                            auth,
                            filtered_url_list[0][1]
                        )
                    except UnauthorizedForResourceError:
                        # User is not authorized, raise a 401-error
                        abort(401)
                    except ResourceForbiddenError:
                        # User is not authorized, raise a 403-error
                        abort(403)
                    except ResourceNotFoundError:
                        # User is not authorized, raise a 404-error
                        abort(404)

                    # Paginate the result (if requested)
                    if return_value.paginate and \
                            return_value.type == \
                            ResponseType.RESOURCE_SET and \
                            hasattr(return_value.data, '__len__'):

                        # Set the total items, limit and the page
                        return_value.limit = limit
                        return_value.page = page
                        return_value.total_items = return_value.data.__len__()

                        # Calculate the max page
                        return_value.last_page = ceil(
                            return_value.total_items / limit)

                        # Check if the page is correct, and if it
                        # isn't, fix it
                        if return_value.page > return_value.last_page:
                            return_value.page = return_value.last_page
                        elif return_value.page < 1:
                            return_value.page = 1

                        # Calculate the start and end index for the
                        # results
                        start = (return_value.page - 1) * limit
                        end = start + limit

                        # Filter the data
                        return_value.data = return_value.data[start:end]

                    # Add 'pretty' JSON results, if the user requested it
                    json_options = dict()
                    if pretty:
                        json_options = {
                            'indent': 4,
                            'sort_keys': True
                        }

                    # Return the result
                    return Response(
                        response=dumps(
                            return_value, cls=RESTAPIJSONEncoder,
                            **json_options
                        ),
                        mimetype='application/json'
                    )

            # No matching URL found for this HTTP method. We abort the
            # request with a 404 error
            abort(404)

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

    def register_authorization_method(
        self,
        func: Callable[[str, Optional[List[str]]], RESTAPIAuthorization]
    ) -> None:
        """ Method to set a authorization method for the REST API.
            Should be used as a decorator

            Parameter
            ---------
            func : Callable[[str, Optional[List[str]]],
                   RESTAPIAuthorization]
                Function that takes in two variables (one for the
                authorization data and one for the requested
                permission). Should return a RESTAPIAuthorization
                object that defines if the request is authorized or
                not.

            Returns
            -------
            None
        """
        self.authorization_function = func

    def get_all_endpoints(self) -> List[RESTAPIEndpointURL]:
        """ Method that returns all RESTAPIEndpoints for this REST API
            in a list with RESTAPIEndpointURL objects.

            Parameter
            ---------
            None

            Returns
            -------
            list[RESTAPIEndpointURL]
                A list with RESTAPIEndpointURLs for this REST API.
        """

        # Create a empty list that we can return later on
        return_list: List[RESTAPIEndpointURL] = list()

        # Add endpoints from groups.
        for group in self.groups:
            return_list += group.get_endpoints()

        # Return the list
        return return_list
# ---------------------------------------------------------------------
