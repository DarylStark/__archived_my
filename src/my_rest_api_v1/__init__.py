"""
    The my_rest_api_v1 package is the main package that will be used
    for the REST API v1 service of the `my-dstark-nl` application. It
    will contain the application code that starts the REST API and run
    the REST API.
"""
# ---------------------------------------------------------------------
# Imports
from typing import List, Optional
from flask import Flask
from rest_api_generator import RESTAPIGenerator, RESTAPIAuthorization
from rich.logging import RichHandler
import logging
from my_rest_api_v1.api import api_group_api
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
def auth(auth: str, scopes: Optional[List[str]]) -> RESTAPIAuthorization:
    # Create a authorization object
    auth_object: RESTAPIAuthorization = RESTAPIAuthorization()

    # Temporary API tokens
    tokens = {
        'token_a': {
            'scopes': ['api.ping'],
            'data': {'id': 2, 'username': 'daryl.stark'}
        }
    }

    # Get the API token
    token = auth.split()[1]

    # Check scopes
    try:
        token_object = tokens[token]
        for scope in scopes:
            if scope in token_object['scopes']:
                auth_object.authorized = True
                auth_object.data = token_object['data']
    except KeyError:
        pass

    # Return authorization object
    return auth_object


# Register the created groups
my_rest_api_v1.register_group(group=api_group_api)

# The RESTAPIGenerator object works with a Blueprint object that can be
# added to the Flask app. By doing this.
flask_app.register_blueprint(my_rest_api_v1.blueprint)
# ---------------------------------------------------------------------
if __name__ == '__main__':
    raise NotImplementedError('This file can not be ran as script')
# ---------------------------------------------------------------------
