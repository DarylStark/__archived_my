""" Module that creates the Flask Blueprint for the data of the My
    Ganymade service. This is the backend for the My Ganymade service.
"""

from flask.blueprints import Blueprint
from flask import Response, request
from json import dumps

blueprint_data = Blueprint(
    name='my_ganymade_backend',
    import_name=__name__,
    url_prefix='/data/'
)


@blueprint_data.route(
    '/',
    methods=['GET']
)
def index() -> str:
    """ Homepage for the 'data' part of the application. """
    return 'Data homepage'


@blueprint_data.route(
    '/aaa/login',
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
