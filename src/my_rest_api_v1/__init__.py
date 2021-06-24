"""
    The my_rest_api_v1 package is the main package that will be used
    for the REST API v1 service of the `my-dstark-nl` application. It
    will contain the application code that starts the REST API and run
    the REST API.
"""
# ---------------------------------------------------------------------
# Imports
from os import environ
from typing import List, Optional, Union
from flask import Flask
import my_database
from my_rest_api_v1.exceptions import ConfigNotLoadedError, \
    EnvironmentNotSetError
from rest_api_generator import RESTAPIGenerator
from rich.logging import RichHandler
from my_rest_api_v1.api import api_group_api
from my_rest_api_v1.users import api_group_users
import logging
from my_rest_api_v1.authorization import authorization
from config_loader import ConfigLoader
# ---------------------------------------------------------------------
# Load the settings
if not ConfigLoader.load_settings():
    raise ConfigNotLoadedError(
        f'Configuration was not yet loaded.')

# Configure logging
logging.basicConfig(
    level=ConfigLoader.config['logging']['level'],
    format='%(name)s: %(message)s',
    datefmt="[%X]",
    handlers=[RichHandler()]
)

# Create a logger for the My REST API package
logger = logging.getLogger('MyRESTAPI')

# Create a Flask object
logger.debug('Creating Flask object')
flask_app = Flask(__name__)

# Create a RESTAPIGenerator object
logger.debug('Creating RESTAPIGenerator object')
my_rest_api_v1 = RESTAPIGenerator(
    bp_name='my_rest_api_v1',
    bp_import_name=__name__,
    bp_url_prefix='/api/v1/')

# Turn on authorization and set the authorization method
logger.debug('Configuring authorization for RESTAPIGenerator')
my_rest_api_v1.use_authorization = True
my_rest_api_v1.authorization_function = authorization

# Make sure errors get reported as JSON error resposne instead of
# normal Flask error pages
my_rest_api_v1.abort_on_error = False

# Enable the correct methods
methods = ('GET', 'PATCH', 'POST', 'DELETE')
logger.debug(f'Setting accpted HTTP methods: {", ".join(methods)}')
for method in methods:
    my_rest_api_v1.accept_method(method)

# Register the created groups
logger.debug('Registering groups')
my_rest_api_v1.register_group(group=api_group_api)
my_rest_api_v1.register_group(group=api_group_users)

# The RESTAPIGenerator object works with a Blueprint object that can be
# added to the Flask app. By doing this.
logger.debug('Adding REST API blueprint to the Flask app')
flask_app.register_blueprint(my_rest_api_v1.blueprint)
# ---------------------------------------------------------------------
