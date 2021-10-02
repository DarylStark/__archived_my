""" Module that creates the Flask Blueprint for the aaa data of the
    My Ganymede service. This Blueprint can be used to login and
    logout.
"""

from flask.blueprints import Blueprint
from flask.globals import request
from my_ganymade.response import Response
from my_ganymade.data_endpoint import data_endpoint
from json import dumps

# Create the Blueprint
blueprint_data_aaa = Blueprint(
    name='my_ganymade_data_aaa',
    import_name=__name__,
    url_prefix='/data/aaa/'
)


@blueprint_data_aaa.route(
    '/login',
    methods=['POST']
)
@data_endpoint(allowed_users=None)
def login() -> Response:
    """ Method to log a user in. Should receive the username and
        password for the user and (if applicable) the 'second factor'
        code. Return 'success = True' when the credentials match. """

    # Get the given data
    data = request.json

    # Create a data object to return
    return_object = Response()

    if data['second_factor'] is None:
        # Second factor should be given
        return_object.error_code = 1
    else:
        if data['username'] == 'a' and data['password'] == 'b':
            return_object.success = True
        else:
            return_object.success = False
            return_object.error_code = 2

    return return_object
