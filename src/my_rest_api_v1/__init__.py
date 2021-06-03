"""
    The my_rest_api_v1 package is the main package that will be used
    for the REST API v1 service of the `my-dstark-nl` application. It
    will contain the application code that starts the REST API and run
    the REST API.
"""
# ---------------------------------------------------------------------
# Imports
from typing import List, Optional, Union
from flask import Flask
from rest_api_generator import RESTAPIGenerator, RESTAPIAuthorization, \
    BasicAuthorization, BearerAuthorzation
from rich.logging import RichHandler
from my_rest_api_v1.api import api_group_api
import logging
from my_database.api_authorization import get_token_information
# ---------------------------------------------------------------------
# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(message)s',
    datefmt="[%X]",
    handlers=[RichHandler()]
)

# Create a Flask object
flask_app = Flask(__name__)

# Create a RESTAPIGenerator object
my_rest_api_v1 = RESTAPIGenerator(
    bp_name='my_rest_api_v1',
    bp_import_name=__name__,
    bp_url_prefix='/api/v1/')

# Turn on authorization
my_rest_api_v1.use_authorization = True

# Make sure errors get reported as JSON error resposne instead of
# normal Flask error pages
my_rest_api_v1.abort_on_error = False

# Enable the correct methods
my_rest_api_v1.accept_method('POST')
my_rest_api_v1.accept_method('PATCH')
my_rest_api_v1.accept_method('DELETE')


# Create a method for authorization
@my_rest_api_v1.register_authorization_method
def auth(auth: Optional[Union[BasicAuthorization, BearerAuthorzation]],
         scopes: Optional[List[str]]) -> RESTAPIAuthorization:
    """
        Method that does the authentication for the REST API.

        Parameters
        ----------
        auth : Optional[Union[BasicAuthorization, BearerAuthorzation]]
            The authentication header from the Flask Request. Can be
            None, a BasicAuthorization object or a BearerAuthorization
            object, depending on the given authorization.

        scopes : Optional[List[str]]
            The scopes that are defined in the endpoint that are
            required for this endpoint.

        Returns
        -------
        RESTAPIAuthorization:
            A object containing the authorization information.
    """

    # Create a authorization object
    auth_object: RESTAPIAuthorization = RESTAPIAuthorization()

    # Check the type of authorization we received. We only accept the
    # 'Bearer' kind, since that is being used in OAuth world.
    if type(auth) is not BearerAuthorzation:
        return auth_object

    # Get the token object
    token_object = get_token_information(auth.token)

    # If we didn't get a object, the token is wrong
    if token_object is None:
        auth_object.authorized = False
        return auth_object

    # Get the assosicated scopes
    token_scopes = [
        token_scope.scope.full_scope_name
        for token_scope in token_object.token_scopes
    ]

    # Check if any of the given scopes is in the 'token scopes'
    for scope in scopes:
        if scope in token_scopes:
            auth_object.authorized = True
            auth_object.data = token_object
            break

    # Return authorization object
    return auth_object


# Register the created groups
my_rest_api_v1.register_group(group=api_group_api)

# The RESTAPIGenerator object works with a Blueprint object that can be
# added to the Flask app. By doing this.
flask_app.register_blueprint(my_rest_api_v1.blueprint)
# ---------------------------------------------------------------------
