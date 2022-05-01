""" Module that creates the Flask Blueprint for the account data
    of the My Web UI service. This Blueprint can be used to set
    account details for the currently logged on user.
"""

from json import dumps
from typing import Optional
from flask.blueprints import Blueprint
from flask.globals import request, session
from my_database import validate_input
from my_database.auth import (create_user_session, delete_user_sessions,
                              validate_credentials)
from my_database.exceptions import (AuthCredentialsError,
                                    AuthUserRequiresSecondFactorError,
                                    FieldNotValidatedError, IntegrityError)
from my_database.users import update_user, validation_fields
from my_database_model import User
from my_database_model.user_session import UserSession
from my_web_ui.data_endpoint import EndpointPermissions, data_endpoint
from my_web_ui.exceptions import InvalidInputError
from my_web_ui.response import Response

# Create the Blueprint
blueprint_data_user_account = Blueprint(
    name='my_web_ui_data_user_account',
    import_name=__name__,
    url_prefix='/data/user_account/'
)


@blueprint_data_user_account.route(
    '/set_account_details',
    methods=['POST']
)
@data_endpoint(
    allowed_users=EndpointPermissions(
        logged_out_users=False,
        normal_users=True,
        admin_users=True,
        root_users=True))
def set_account_details(user_session: Optional[UserSession]) -> Response:
    """ Method that returns the details about the current user session
        and logged on user-account """

    # Get the given data
    post_data = request.json

    # Validate the given fields
    required_fields = None

    # Set the optional fields
    optional_fields = {
        'fullname': validation_fields['fullname'],
        'username': validation_fields['username'],
        'email': validation_fields['email']
    }

    try:
        # Validate the user input
        validate_input(
            input_values=post_data,
            required_fields=required_fields,
            optional_fields=optional_fields)
    except (TypeError, FieldNotValidatedError) as e:
        raise InvalidInputError(e)

    # Create a data object to return
    return_object = Response(success=False)

    if user_session is not None:
        try:
            changed_resource = update_user(
                req_user=user_session.user,
                user_id=user_session.user_id,
                **post_data
            )
        except IntegrityError:
            # Set the return value to False
            return_object.error_code = 1
            return_object.success = False
        else:
            # Set the return value to True
            return_object.success = True

    # Return the created object
    return return_object
