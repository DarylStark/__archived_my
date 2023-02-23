""" Module that creates the Flask Blueprint for the API token data
    of the My Web UI service. This Blueprint can be used to create,
    retrieve, update or delete API tokens
"""

from typing import Optional
from flask.blueprints import Blueprint
from flask.globals import request
from my_database import validate_input
from my_database.api_clients import get_api_clients
from my_database.api_tokens import create_api_token, get_api_tokens, update_api_token, validation_fields
from my_database.exceptions import FieldNotValidatedError, IntegrityError, NotFoundError
from my_database_model import UserSession
from my_web_ui.data_endpoint import EndpointPermissions, data_endpoint
from my_web_ui.exceptions import InvalidInputError, ResourceIntegrityError, ServerError
from my_web_ui.response import Response

# Create the Blueprint
blueprint_data_api_tokens = Blueprint(
    name='my_web_ui_data_api_tokens',
    import_name=__name__,
    url_prefix='/data/api_tokens/'
)


@blueprint_data_api_tokens.route(
    '/create',
    methods=['POST']
)
@data_endpoint(
    allowed_users=EndpointPermissions(
        logged_out_users=False,
        normal_users=True,
        admin_users=True,
        root_users=True))
def create(user_session: Optional[UserSession]) -> Response:
    """ Method to create API tokens. Should recieve the session id and the
        new data """

    # Get the given data
    post_data = request.json

    # Validate the given fields
    required_fields = {
        'app_token': validation_fields['app_token'],
        'scopes': validation_fields['scopes']
    }

    # Set the optional fields
    optional_fields = {
        'title': validation_fields['title']
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

    # Remove the resources
    if user_session is not None:
        try:
            # Find the ID of the application
            api_client = get_api_clients(req_user=user_session.user,
                                         flt_token=post_data['app_token'])
            post_data.pop('app_token')
            post_data['client_id'] = api_client.id

            # Create the token
            new_object = create_api_token(
                req_user=user_session.user,
                **post_data
            )

            # Set the token in the object
            return_object.data = new_object
            return_object.success = True
        except IntegrityError as err:
            # Integrity errors happen mostly when the token already
            # exists.
            raise ResourceIntegrityError(err)
        except Exception as err:
            # Every other error should result in a ServerError.
            raise ServerError(err)

    # Return the created object
    return return_object


@blueprint_data_api_tokens.route(
    '/all/<int:client_id>',
    methods=['GET']
)
@data_endpoint(
    allowed_users=EndpointPermissions(
        logged_out_users=False,
        normal_users=True,
        admin_users=True,
        root_users=True))
def retrieve_specific(user_session: Optional[UserSession], client_id: int) -> Response:
    """ Method that returns a specific API token. """

    # Create a data object to return
    return_object = Response(success=False)

    if user_session is not None:
        try:
            # Get the API client from the database
            resources = get_api_tokens(
                req_user=user_session.user,
                flt_client_id=client_id
            )

            # Set the tag in the return object
            return_object.data = resources
        except NotFoundError as err:
            # If no resource are found, we set the 'data' in the return object
            # to a empty list.
            return_object.data = []
        except Exception as err:
            # Every other error should result in a ServerError.
            raise ServerError(err)

        # Set the return value to True
        return_object.success = True

    # Return the created object
    return return_object


@blueprint_data_api_tokens.route(
    '/add_permissions',
    methods=['PATCH']
)
@data_endpoint(
    allowed_users=EndpointPermissions(
        logged_out_users=False,
        normal_users=True,
        admin_users=True,
        root_users=True))
def add_permissions(user_session: Optional[UserSession]) -> Response:
    """ Method to create add permissions to API tokens """

    # Get the given data
    post_data = request.json

    # Validate the given fields
    required_fields = {
        'api_token': validation_fields['api_token'],
        'scopes': validation_fields['scopes']
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

    # Remove the resources
    if user_session is not None:
        try:
            # Find the ID of the application
            api_token = get_api_tokens(req_user=user_session.user,
                                       flt_token=post_data['api_token'])

            resource = update_api_token(
                req_user=user_session.user,
                api_token_id=api_token.id,
                **post_data)

            # Set the token in the object
            return_object.data = resource
            return_object.success = True
        except IntegrityError as err:
            # Integrity errors happen mostly when the token already
            # exists.
            raise ResourceIntegrityError(err)
        except Exception as err:
            # Every other error should result in a ServerError.
            raise ServerError(err)

    # Return the created object
    return return_object
