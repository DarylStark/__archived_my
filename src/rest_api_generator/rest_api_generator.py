"""
    This module includes the RESTAPIGenerator class that can be used to
    generate the REST API blueprint
"""
# ---------------------------------------------------------------------
# Imports
from flask import Blueprint
from typing import Optional
# ---------------------------------------------------------------------


class RESTAPIGenerator:
    """ Class that can be used to generate APIs """

    def __init__(self,
                 bp_name: str = 'api_generator',
                 bp_import_name: str = __name__,
                 bp_url_prefix: Optional[str] = None) -> None:
        """ The initiator can be used to configure the Flask Blueprint
        """

        # Create a Flask Blueprint. This can be used to connect the
        # REST API to a existing Flask app
        self.blueprint = Blueprint(
            bp_name, bp_import_name, url_prefix=bp_url_prefix)

        # Create a list with acceptable HTTP methods. By default, we
        # only accept 'GET' requests. The user can add methods to
        # accept.
        self.accepted_http_methods = [
            'GET'
        ]

        # Register the routes
        self.register_routes()

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

    def register_routes(self) -> None:
        """ Method to register the routes for the Blueprint """

        # We create a callback method for the Blueprint and make sure
        # the Flask routing redirects every request to this method.
        @self.blueprint.route('/', defaults={'path': ''},
                              methods=self.accepted_http_methods)
        @self.blueprint.route('/<path:path>',
                              methods=self.accepted_http_methods)
        def execute_url(path: str):
            return f'Requested path: {path}'

    @property
    def flask_blueprint(self) -> Blueprint:
        """ Property that returns the blueprint """
        return self.blueprint
# ---------------------------------------------------------------------
