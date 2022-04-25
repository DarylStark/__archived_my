""" Module that creates the Flask Blueprint for the userssesions data
    of the My Web UI service. This Blueprint can be used to get
    information about user sessions.
"""

from typing import Optional
from flask.blueprints import Blueprint
from flask.globals import request, session
from my_database.exceptions import (AuthUserRequiresSecondFactorError,
                                    AuthCredentialsError)
from my_database_model import User
from my_database_model.user_session import UserSession
from my_web_ui.exceptions import InvalidInputError
from my_web_ui.response import Response
from my_web_ui.data_endpoint import data_endpoint, EndpointPermissions
from my_database.auth import (validate_credentials, create_user_session,
                              delete_user_sessions)
from json import dumps

# Create the Blueprint
blueprint_data_user_sessions = Blueprint(
    name='my_web_ui_data_user_sessions',
    import_name=__name__,
    url_prefix='/data/user_sessions/'
)


@blueprint_data_user_sessions.route(
    '/current',
    methods=['GET']
)
@data_endpoint(
    allowed_users=EndpointPermissions(
        logged_out_users=False,
        normal_users=True,
        admin_users=True,
        root_users=True))
def current_usersession(user_session: Optional[UserSession]) -> Response:
    """ Method that returns the details about the current user session
        and logged on user-account """

    # Create a data object to return
    return_object = Response(success=False)

    if user_session is not None:
        # Set the user session in the return object
        return_object.data = {
            'session': user_session,
            'user_account': user_session.user
        }

        # Set the return value to True
        return_object.success = True

    # Return the created object
    return return_object
