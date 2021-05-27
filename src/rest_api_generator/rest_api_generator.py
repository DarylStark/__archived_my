"""
    This module includes the RESTAPIGenerator class that can be used to
    generate the REST API blueprint.
"""
# ---------------------------------------------------------------------
# Imports
import re
import timeit
import time
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

            Parameters
            ----------
            bp_name : str (default = 'api_generator')
                The name that will be used to create the Blueprint

            bp_import_name : str (default = __name__)
                The import name that will be used to create the
                Blueprint

            bp_url_prefix: Optional[str] (default = None)
                The url prefix for the Blueprint. Will be used by Flask
                to route all the requests.

            Returns
            -------
            None
        """

        # Create a empty set with registered groups. The user can add
        # groups with the 'register_group' command. We make this a set
        # to make sure no groups are added more then once.
        self.groups: Set[RESTAPIGroup] = set()

        # Create a Flask Blueprint. This can be used to connect the
        # REST API to a existing Flask app
        self.blueprint: Blueprint = Blueprint(
            name=bp_name,
            import_name=bp_import_name,
            url_prefix=bp_url_prefix
        )

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
        self.abort_on_error: bool = False

        # Register the routes
        self.add_routes()

    def accept_method(self, method: str) -> None:
        """ Method to add HTTP methods to the accepted list

            Parameters
            ----------
            method : str
                The method to add ('GET', for example).

            Returns
            -------
            None
        """
        self.accepted_http_methods.append(method)

    def deny_method(self, method: str) -> None:
        """ Method to remove HTTP methods from the accepted list.

            Parameters
            ----------
            method : str
                The method to add ('GET', for example).

            Returns
            -------
            None
        """

        try:
            self.accepted_http_methods.remove(method)
        except ValueError:
            # If the item wasn't in the list, we get an ValueError
            # exception. We don't do anything in that case.
            pass

    def raise_error(self,
                    code: int,
                    msg: Optional[str] = None
                    ) -> Optional[RESTAPIResponse]:
        """ Method that either aborts the request, or returns a
            RESTAPIRespone with a error code.

            Parameters
            ----------
            code : int
                The HTTP error code for this error.

            msg : Optional[str]
                The message to append

            Returns
            -------
            None
        """

        # If the 'abort_on_error' is set to True, we abort the request
        # with the given parameter
        if self.abort_on_error:
            abort(code)

        # Otherwise, we create a RESTAPIResponse that we can return
        if not self.abort_on_error:
            error_response = RESTAPIResponse(ResponseType.ERROR)
            error_response.error_code = code
            error_response.error_message = msg
            error_response.success = False
            return error_response

    def add_routes(self) -> None:
        """ Method to register the routes for the Blueprint.

            Parameters
            ----------
            None

            Returns
            -------
            None
        """

        # We create a callback method for the Blueprint and make sure
        # the Flask routing redirects every request to this method.
        @self.blueprint.route('/', defaults={'path': ''},
                              methods=self.accepted_http_methods)
        @self.blueprint.route('/<path:path>',
                              methods=self.accepted_http_methods)
        def execute_url(path: str) -> Optional[Union[str, Response]]:
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
            # Get the starttime
            time_start = timeit.default_timer()

            # Get a list of all endpoints registered in this REST API
            url_list: List[RESTAPIEndpointURL] = self.get_all_endpoints()

            # Filter the list to only include the URL that we need
            filtered_url_list = [
                (endpoint, re.fullmatch(endpoint.url, path))
                for endpoint in url_list
                if re.fullmatch(endpoint.url, path)
            ]

            # Set JSON options
            json_options = dict()

            # Add 'pretty' JSON results, if the user requested it
            pretty: bool = self.default_pretty
            if 'pretty' in request.args.keys():
                pretty = True

            if pretty:
                json_options = {
                    'indent': 4,
                    'sort_keys': True
                }

            # Set empty return value
            return_value: Optional[RESTAPIResponse] = None

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
                    error_return: Optional[RESTAPIResponse] = None

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
                                    endpoint.auth_scopes.__getattribute__(
                                        request.method)
                                )
                        except (AttributeError, KeyError):
                            auth = RESTAPIAuthorization(authorized=False)

                        # Check the given value. If the user is not
                        # authorized, we raise a 403 error
                        if not auth.authorized:
                            error = self.raise_error(403)
                            if error:
                                error_return = error
                            else:
                                return None

                    # Get the variables given in the URL (if any are
                    # given).
                    page: int = 1
                    limit: int = self.default_limit

                    if 'page' in request.args.keys():
                        page = int(request.args['page'])
                    if 'limit' in request.args.keys():
                        limit = int(request.args['limit'])

                    # Done! Run the endpoint method
                    try:
                        if error_return:
                            return_value = error_return
                        else:
                            return_value = endpoint.func(
                                auth,
                                filtered_url_list[0][1]
                            )
                    except UnauthorizedForResourceError as exception:
                        # User is not authorized, raise a 401-error
                        error = self.raise_error(401, str(exception))
                        if error:
                            return_value = error
                        else:
                            return None
                    except ResourceForbiddenError as exception:
                        # User is not authorized, raise a 403-error
                        error = self.raise_error(401, str(exception))
                        if error:
                            return_value = error
                        else:
                            return None
                    except ResourceNotFoundError as exception:
                        # User is not authorized, raise a 404-error
                        error = self.raise_error(401, str(exception))
                        if error:
                            return_value = error
                        else:
                            return None

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
            else:
                # No matching URL found for this HTTP method. We abort the
                # request with a 404 error
                error = self.raise_error(404, 'Endpoint not found')
                if error:
                    return_value = error
                else:
                    return None

            # Get the end time and calculate the runtime in ms
            time_end = timeit.default_timer()
            return_value.runtime = (time_end - time_start) * 1000

            # Return the result
            return Response(
                response=dumps(
                    return_value, cls=RESTAPIJSONEncoder,
                    **json_options
                ),
                mimetype='application/json'
            )

    def register_group(self, group: RESTAPIGroup) -> None:
        """ Method to register a group for the REST API

            Parameters
            ----------
            group : RESTAPIGroup
                The group to register

            Returns
            -------
            None
        """

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
                scopes). Should return a RESTAPIAuthorization
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
