"""
    The my_rest_api_v1 package is the main package that will be used
    for the REST API v1 service of the `my-dstark-nl` application. It
    will contain the application code that starts the REST API and run
    the REST API.
"""
# ---------------------------------------------------------------------
# Imports
from flask import Flask
from rest_api_generator import RESTAPIGenerator, RESTAPIGroup
from my_rest_api_v1.api_group_users import APIGroupUsers
# ---------------------------------------------------------------------
# Create a Flask object
flask_app = Flask(__name__)

# Create a RESTAPIGenerator object
my_rest_api_v1 = RESTAPIGenerator(
    bp_name='my_rest_api_v1',
    bp_import_name=__name__,
    bp_url_prefix='/api/v1/')

# Create a REST API group for users
api_group_users = APIGroupUsers()

# Register the created groups
my_rest_api_v1.register_group(group=api_group_users.rest_api_group)

# The RESTAPIGenerator object works with a Blueprint object that can be
# added to the Flask app. By doing this.
flask_app.register_blueprint(my_rest_api_v1.blueprint)
# ---------------------------------------------------------------------
if __name__ == '__main__':
    raise NotImplementedError('This file can not be ran as script')
# ---------------------------------------------------------------------
