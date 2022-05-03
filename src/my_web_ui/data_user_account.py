""" Module that creates the Flask Blueprint for the account data
    of the My Web UI service. This Blueprint can be used to set
    account details for the currently logged on user.
"""

from json import dumps
from typing import Optional
from flask.blueprints import Blueprint
from flask.globals import request, session
from pyotp import TOTP
from my_database import validate_input
from my_database.auth import (create_user_session, delete_user_sessions,
                              validate_credentials)
from my_database.exceptions import (AuthCredentialsError,
                                    AuthUserRequiresSecondFactorError,
                                    FieldNotValidatedError, IntegrityError)
from my_database.field import Field
from my_database.users import update_user, update_user_2fa_secret, update_user_disable_2fa, update_user_password, validation_fields
from my_database_model import User
from my_database_model.user_session import UserSession
from my_web_ui.data_endpoint import EndpointPermissions, data_endpoint
from my_web_ui.exceptions import InvalidInputError, PermissionDeniedError
from my_web_ui.response import Response

# Create the Blueprint
blueprint_data_user_account = Blueprint(
    name='my_web_ui_data_user_account',
    import_name=__name__,
    url_prefix='/data/user_account/'
)

# Dict with temporary 2FA codes
tfa_codes = dict()


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
    """ Method to set user account details """

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


@blueprint_data_user_account.route(
    '/update_password',
    methods=['POST']
)
@data_endpoint(
    allowed_users=EndpointPermissions(
        logged_out_users=False,
        normal_users=True,
        admin_users=True,
        root_users=True))
def update_password(user_session: Optional[UserSession]) -> Response:
    """ Method to update the password for a user """

    # Get the given data
    post_data = request.json

    # Validate the given fields
    required_fields = {
        'current_password': validation_fields['password'],
        'new_password': validation_fields['password'],
    }

    # Set the optional fields
    optional_fields = None

    try:
        # Validate the user input
        validate_input(
            input_values=post_data,
            required_fields=required_fields,
            optional_fields=optional_fields)
    except (TypeError, FieldNotValidatedError) as e:
        raise InvalidInputError(e)

    # Check if current password is correct
    if not user_session.user.verify_password(post_data['current_password']):
        # User tries to change the password but gave the wrong current password
        raise PermissionDeniedError('Current password is not correct')

    # Create a data object to return
    return_object = Response(success=False)

    if user_session is not None:
        try:
            changed_resource = update_user_password(
                req_user=user_session.user,
                user_id=user_session.user_id,
                password=post_data['new_password']
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


@blueprint_data_user_account.route(
    '/get_2fa_code',
    methods=['GET']
)
@data_endpoint(
    allowed_users=EndpointPermissions(
        logged_out_users=False,
        normal_users=True,
        admin_users=True,
        root_users=True))
def get_2fa_code(user_session: Optional[UserSession]) -> Response:
    """ Method to retrieve a temporary 2FA code """

    # Check if the user already has a 2FA code
    if user_session.user.second_factor:
        raise PermissionDeniedError('This user already has a second factor')

    # Create a data object to return
    return_object = Response(success=False)

    if user_session is not None:
        # Generate a new 2FA code and add it to the global list of temporary
        # 2FA codes
        username = user_session.user.username
        tfa_codes[username] = user_session.user.get_random_second_factor()

        # Set the code in the object that we return
        return_object.data = {'code': tfa_codes[user_session.user.username]}

        # Set the object to a success
        return_object.success = True

    # Return the created object
    return return_object


@blueprint_data_user_account.route(
    '/verify_2fa_code',
    methods=['POST']
)
@data_endpoint(
    allowed_users=EndpointPermissions(
        logged_out_users=False,
        normal_users=True,
        admin_users=True,
        root_users=True))
def verify_2fa_code(user_session: Optional[UserSession]) -> Response:
    """ Method to verify a temporary 2FA code """

    # Check if the user already has a 2FA code
    if user_session.user.second_factor:
        raise PermissionDeniedError('This user already has a second factor')

    # Check if the user has a temporary code
    if user_session.user.username not in tfa_codes.keys():
        raise PermissionDeniedError(
            'A temporary code should be generated first by using the `get_2fa_code` endpoint')

    # Get the given data
    post_data = request.json

    # Validate the given fields
    required_fields = {
        'code': Field('code', str, '[0-9]{6}')
    }

    # Set the optional fields
    optional_fields = None

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
        # Check if the given code is correct
        username = user_session.user.username
        secret = tfa_codes[username]

        # Verify
        return_object.success = False
        if TOTP(secret).now() == post_data['code']:
            # Set the code in the userobject
            try:
                changed_resource = update_user_2fa_secret(
                    req_user=user_session.user,
                    user_id=user_session.user_id,
                    secret=secret
                )
            except IntegrityError:
                # Set the return value to False
                return_object.error_code = 1
                return_object.success = False
            else:
                # Set the return value to True
                return_object.success = True
        else:
            raise PermissionDeniedError('TOTP code is not correct')

    # Return the created object
    return return_object


@blueprint_data_user_account.route(
    '/disable_2fa',
    methods=['GET']
)
@data_endpoint(
    allowed_users=EndpointPermissions(
        logged_out_users=False,
        normal_users=True,
        admin_users=True,
        root_users=True))
def disable_2fa(user_session: Optional[UserSession]) -> Response:
    """ Method to disable 2FA on a account """

    # Check if the user already has a 2FA code
    if not user_session.user.second_factor:
        raise PermissionDeniedError(
            'This user already has two factor authentication disabled')

    # Create a data object to return
    return_object = Response(success=False)

    if user_session is not None:
        return_object.success = False
        try:
            changed_resource = update_user_disable_2fa(
                req_user=user_session.user,
                user_id=user_session.user_id
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
