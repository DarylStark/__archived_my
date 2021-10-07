""" Module that creates the Flask Blueprint for the aaa data of the
    My Ganymede service. This Blueprint can be used to login and
    logout.
"""

from flask.blueprints import Blueprint
from flask.globals import request, session
from my_database.exceptions import (AuthUserRequiresSecondFactorError,
                                    AuthCredentialsError)
from my_database_model import User
from my_ganymede.exceptions import InvalidInputError
from my_ganymede.response import Response
from my_ganymede.data_endpoint import data_endpoint, EndpointPermissions
from my_database.auth import validate_credentials, create_user_session
from json import dumps

# Create the Blueprint
blueprint_data_aaa = Blueprint(
    name='my_ganymede_data_aaa',
    import_name=__name__,
    url_prefix='/data/aaa/'
)


@blueprint_data_aaa.route(
    '/login',
    methods=['POST']
)
@data_endpoint(
    allowed_users=EndpointPermissions(
        logged_out_users=True,
        normal_users=False,
        admin_users=False,
        root_users=False))
def login() -> Response:
    """ Method to log a user in. Should receive the username and
        password for the user and (if applicable) the 'second factor'
        code. Return 'success = True' when the credentials match. """

    # Get the given data
    data = request.json

    # Validate the given fields
    needed_fields = ['username', 'password', 'second_factor']
    for field in needed_fields:
        if field not in data.keys():
            raise InvalidInputError(f'Missing field "{field}"')

    # Create a data object to return
    return_object = Response()

    # Create dict to send to the my_database package
    data_dict = {
        'username': data['username'],
        'password': data['password']
    }

    # If a 'second factor' is given, we can pass that too
    if data['second_factor'] is not None:
        data_dict['second_factor'] = data['second_factor']

    # Check the username
    try:
        user_object = validate_credentials(**data_dict)
    except AuthUserRequiresSecondFactorError:
        # Second factor is needed or the username is not found. In both
        # cases we return to the client that a second factor is needed.
        # If someone tries to login with a non-existing username, he
        # does not find out that username is non-existing
        return_object.success = False
        return_object.error_code = 1
    except AuthCredentialsError:
        # Second factor is needed or the username is not found. In both
        # cases we return to the client that a second factor is needed.
        # If someone tries to login with a non-existing username, he
        # does not find out that username is non-existing
        return_object.success = False
        return_object.error_code = 2
    else:
        if type(user_object) is User:
            # Credentials were correct. We update the return dict
            return_object.success = True
            return_object.error_code = None

            # Create a User Session object
            user_session = create_user_session(
                req_user=user_object,
                host=request.remote_addr)

            # Then we create a Flask Session; this session will contain the
            # ID of the session and the secret for the session. We will
            # verify these with the database when the user tries to
            # retrieve a protected page.
            session['sid'] = user_session.id
            session['secret'] = user_session.secret
        else:
            # Something weird is going on
            return_object.success = False
            return_object.error_code = 3

    return return_object
