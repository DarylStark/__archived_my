""" Module that creates the Flask Blueprint for the userssesions data
    of the My Web UI service. This Blueprint can be used to get
    information about user sessions.
"""

from json import dumps
from typing import Optional
from flask.blueprints import Blueprint
from flask.globals import request, session
from my_database import validate_input
from my_database.user_sessions import (delete_user_sessions, get_user_sessions,
                                       update_user_session, validation_fields)
from my_database.exceptions import (AuthCredentialsError,
                                    AuthUserRequiresSecondFactorError,
                                    FieldNotValidatedError, NotFoundError)
from my_database_model import User
from my_database_model.user_session import UserSession
from my_web_ui.data_endpoint import EndpointPermissions, data_endpoint
from my_web_ui.exceptions import InvalidInputError, ServerError
from my_web_ui.response import Response

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
def current(user_session: Optional[UserSession]) -> Response:
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


@blueprint_data_user_sessions.route(
    '/all',
    methods=['GET']
)
@data_endpoint(
    allowed_users=EndpointPermissions(
        logged_out_users=False,
        normal_users=True,
        admin_users=True,
        root_users=True))
def retrieve(user_session: Optional[UserSession]) -> Response:
    """ Method that returns all the user sessions for the logged on user """

    # Create a data object to return
    return_object = Response(success=False)

    if user_session is not None:
        try:
            # Get the user sessions from the database
            resources = get_user_sessions(
                req_user=user_session.user
            )

            # Set the user session in the return object
            return_object.data = resources
        except NotFoundError as err:
            # If no resources are found, we set the 'data' in the return object
            # to a empty list. This should never happen since this endpoint can
            # only be called when a session exists
            return_object.data = []
        except Exception as err:
            # Every other error should result in a ServerError.
            raise ServerError(err) from err

        # Set the return value to True
        return_object.success = True

    # Return the created object
    return return_object


@blueprint_data_user_sessions.route(
    '/update',
    methods=['PATCH']
)
@data_endpoint(
    allowed_users=EndpointPermissions(
        logged_out_users=False,
        normal_users=True,
        admin_users=True,
        root_users=True))
def update(user_session: Optional[UserSession]) -> Response:
    """ Method to update user sessions. Should recieve the session id and the
        new title """

    # Get the given data
    post_data = request.json

    # Validate the given fields
    required_fields = {
        'session_id': validation_fields['session_id'],
        'title': validation_fields['title']
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
        raise InvalidInputError(e) from e

    # Delete `session_id` from the post_data dict. If we don't do this, we can't
    # use the `post_data` dict as input for the backend
    session_id = post_data['session_id']
    post_data.pop('session_id')

    # Create a data object to return
    return_object = Response(success=False)

    # Remove the resources
    if user_session is not None:
        try:
            # Get the user sessions from the database
            update_user_session(
                req_user=user_session.user,
                user_session_id=session_id,
                **post_data
            )

            # We create a key for the return object that will say that the data
            # is removed
            return_object.data = {'update': True}
        except NotFoundError as err:
            # If no sessions are found, we set the data to False
            return_object.data = {'update': False}
        except Exception as err:
            # Every other error should result in a ServerError.
            raise ServerError(err) from err

        # Set the return value to True
        return_object.success = True

    # Return the created object
    return return_object


@blueprint_data_user_sessions.route(
    '/delete',
    methods=['DELETE']
)
@data_endpoint(
    allowed_users=EndpointPermissions(
        logged_out_users=False,
        normal_users=True,
        admin_users=True,
        root_users=True))
def delete(user_session: Optional[UserSession]) -> Response:
    """ Method to remove user sessions. Should receive a list of sessions to
        remove from the user in the POST data """

    # Get the given data
    post_data = request.json

    # Validate the given fields
    required_fields = {
        'session_ids': validation_fields['session_ids'],
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
        raise InvalidInputError(e) from None

    # Create a data object to return
    return_object = Response(success=False)

    # Create dict to send to the my_database package
    data_dict = {
        'req_user': user_session.user,
        'session_id': post_data['session_ids']
    }

    # Remove the resources
    if user_session is not None:
        try:
            # Remove the user sessions from the database
            delete_user_sessions(**data_dict)

            # We create a key for the return object that will say that the data
            # is removed
            return_object.data = {'deleted': True}
        except NotFoundError as err:
            # If no sessions are found, we set the data to False
            return_object.data = {'deleted': False}
        except Exception as err:
            # Every other error should result in a ServerError.
            raise ServerError(err) from err

        # Set the return value to True
        return_object.success = True

    # Return the created object
    return return_object
