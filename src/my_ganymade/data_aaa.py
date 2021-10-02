""" Module that creates the Flask Blueprint for the aaa data of the
    My Ganymede service. This Blueprint can be used to login and
    logout.
"""

from flask.blueprints import Blueprint
from flask import Response, request
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
def login() -> Response:
    """ Method to log a user in. Should receive the username and
        password for the user. """

    # Get the given data
    data = request.json

    # Create a data object to return
    return_object = {
        'success': False,
        'reason': 'unknown'
    }

    if data['second_factor'] is None:
        return_object['reason'] = 'second_factor_needed'
    else:
        if data['username'] == 'a' and data['password'] == 'b':
            return_object['success'] = True
            return_object['reason'] = None
        else:
            return_object['reason'] = 'credentials_invalid'

    return Response(
        response=dumps(return_object),
        status=200,
        mimetype='application/json'
    )
