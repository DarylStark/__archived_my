""" Module that creates the Flask Blueprint for the web ui settings
    of the My Web UI service. This Blueprint can be used to set
    web ui settings for the currently logged on user.
"""

from typing import Optional

from flask.blueprints import Blueprint
from flask.globals import request

from my_database import validate_input
from my_database.exceptions import (FieldNotValidatedError, IntegrityError,
                                    NotFoundError)
from my_database.web_ui_settings import (create_web_ui_setting,
                                         get_web_ui_settings,
                                         update_web_ui_setting,
                                         validation_fields)
from my_database_model.user_session import UserSession
from my_web_ui.data_endpoint import EndpointPermissions, data_endpoint
from my_web_ui.exceptions import InvalidInputError, ServerError
from my_web_ui.response import Response

# Create the Blueprint
blueprint_data_web_ui_settings = Blueprint(
    name='my_web_ui_data_web_ui_settings',
    import_name=__name__,
    url_prefix='/data/web_ui_settings/'
)


@blueprint_data_web_ui_settings.route(
    '/set_setting',
    methods=['POST']
)
@data_endpoint(
    allowed_users=EndpointPermissions(
        logged_out_users=False,
        normal_users=True,
        admin_users=True,
        root_users=True))
def set_setting(user_session: Optional[UserSession]) -> Response:
    """ Method to set a specific setting """

    # Get the given data
    post_data = request.json

    # Validate the given fields
    required_fields = {
        'setting': validation_fields['setting'],
        'value': validation_fields['value']
    }

    # Set the optional fields
    optional_fields = None

    try:
        # Validate the user input
        validate_input(
            input_values=post_data,
            required_fields=required_fields,
            optional_fields=optional_fields)
    except (TypeError, FieldNotValidatedError) as error:
        raise InvalidInputError(error) from None

    # Create a data object to return
    return_object = Response(success=False)

    if user_session is not None:
        try:
            # First, we get the setting
            try:
                setting = get_web_ui_settings(
                    req_user=user_session.user, flt_setting=post_data['setting'])
                print('test')
            except NotFoundError:
                changed_resource = create_web_ui_setting(
                    req_user=user_session.user,
                    **post_data
                )
            else:
                # Found setting; update it!
                changed_resource = update_web_ui_setting(
                    req_user=user_session.user,
                    setting_id=setting.id,
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


@blueprint_data_web_ui_settings.route(
    '/get_settings',
    methods=['GET']
)
@data_endpoint(
    allowed_users=EndpointPermissions(
        logged_out_users=False,
        normal_users=True,
        admin_users=True,
        root_users=True))
def get_settings(user_session: Optional[UserSession]) -> Response:
    """ Method that returns the web ui setting for the logged on user """

    # Create a data object to return
    return_object = Response(success=False)

    if user_session is not None:
        try:
            # Default settings is a empty dictionary
            return_object.data = dict()

            # Get the settings from the database
            settings = get_web_ui_settings(req_user=user_session.user)
            if settings:
                return_object.data = {
                    'settings': {x.setting: x.value for x in settings}
                }
        except NotFoundError as error:
            # If no settings are found, we set the 'data' in the return object
            # to a empty list
            return_object.data = []
        except Exception as error:
            # Every other error should result in a ServerError.
            raise ServerError(error) from error

        # Set the return value to True
        return_object.success = True

    # Return the created object
    return return_object
