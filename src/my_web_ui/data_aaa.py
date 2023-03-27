""" Module that creates the Flask Blueprint for the aaa data of the
    My Web UI service. This Blueprint can be used to login and
    logout.
"""

from typing import Optional

from flask.blueprints import Blueprint
from flask.globals import request, session
from flask import app as flask_app

from my_database.auth import validate_credentials
from my_database.exceptions import (AuthCredentialsError,
                                    AuthUserRequiresSecondFactorError)
from my_database.user_sessions import create_user_session, delete_user_sessions
from my_database_model import User
from my_database_model.user_session import UserSession
from my_web_ui.data_endpoint import EndpointPermissions, data_endpoint
from my_web_ui.exceptions import InvalidInputError
from my_web_ui.response import Response

# Create the Blueprint
blueprint_data_aaa = Blueprint(
    name='my_web_ui_data_aaa',
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
def login(user_session: Optional[UserSession]) -> Response:
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

            # Figure out the remote address of the user. Because
            # this application has to be able to run on Google App
            # Engine, we have to do a little hacking here. GAE uses
            # a webfront end which changes the `request.remote_addr`
            # variable to be `127.0.0.1` always. GAE does however
            # save the IP address if the original client in the
            # `X-Forwarded-For` HTTP header. We check if that
            # header exists, and if it does, we use that for the
            # remote address. Otherwise, we use the remote address
            # that Flask provides
            host_addr = request.remote_addr
            if 'X-Forwarded-For' in request.headers:
                host_addr = request.headers['X-Forwarded-For'].split(',')[0]

            # Create a User Session object
            user_session = create_user_session(
                req_user=user_object,
                host=host_addr)

            # Then we create a Flask Session; this session will contain the
            # ID of the session and the secret for the session. We will
            # verify these with the database when the user tries to
            # retrieve a protected page.
            session.permanent = True
            session['sid'] = user_session.id
            session['secret'] = user_session.secret
        else:
            # Something weird is going on
            return_object.success = False
            return_object.error_code = 3

    return return_object


@blueprint_data_aaa.route(
    '/logout',
    methods=['GET']
)
@data_endpoint(
    allowed_users=EndpointPermissions(
        logged_out_users=False,
        normal_users=True,
        admin_users=True,
        root_users=True))
def logout(user_session: Optional[UserSession]) -> Response:
    """ Method to log a user out. This will delete the UserSession from
        the database and remove the Flask Session cookie """

    # Create a data object to return
    return_object = Response(success=False)

    if user_session is not None:
        # Delete the UserSession
        delete_user_sessions(req_user=user_session.user,
                             session_id=user_session.id)

        # Remote the Flask Session
        session.clear()

        # Set the return value to True
        return_object.success = True

    # Return the created object
    return return_object
