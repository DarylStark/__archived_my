""" Module that creates the Flask Blueprint for the API client data
    of the My Web UI service. This Blueprint can be used to get
    configured API clients
"""

from json import dumps
from typing import Optional
from flask.blueprints import Blueprint
from flask.globals import request, session
from my_database import validate_input
from my_database.api_clients import create_api_client, delete_api_clients, get_api_clients, update_api_client, validation_fields
from my_database.exceptions import (AuthCredentialsError,
                                    AuthUserRequiresSecondFactorError,
                                    FieldNotValidatedError, IntegrityError, NotFoundError)
from my_database_model import User, UserSession, Tag
from my_web_ui.data_endpoint import EndpointPermissions, data_endpoint
from my_web_ui.exceptions import InvalidInputError, ResourceIntegrityError, ServerError
from my_web_ui.response import Response

# Create the Blueprint
blueprint_data_api_clients = Blueprint(
    name='my_web_ui_data_api_clients',
    import_name=__name__,
    url_prefix='/data/api_clients/'
)


@blueprint_data_api_clients.route(
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
    """ Method to create API clients. Should recieve the data for
        the API client """

    # Get the given data
    post_data = request.json

    # Validate the given fields
    required_fields = {
        'app_name': validation_fields['app_name'],
        'app_publisher': validation_fields['app_publisher']
    }

    # Set the optional fields
    optional_fields = {
        'redirect_url': validation_fields['redirect_url']
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
            # Create the tag
            new_object = create_api_client(
                req_user=user_session.user,
                **post_data
            )

            # Set the API client in the object
            return_object.data = new_object
            return_object.success = True
        except IntegrityError as err:
            # Integrity errors happen mostly when the tag already
            # exists.
            raise ResourceIntegrityError(err)
        except Exception as err:
            # Every other error should result in a ServerError.
            raise ServerError(err)

    # Return the created object
    return return_object


@blueprint_data_api_clients.route(
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
    """ Method that returns the API clients """

    # Create a data object to return
    return_object = Response(success=False)

    if user_session is not None:
        try:
            # Get the API client from the database
            resources = get_api_clients(
                req_user=user_session.user
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


@blueprint_data_api_clients.route(
    '/all/<string:token>',
    methods=['GET']
)
@data_endpoint(
    allowed_users=EndpointPermissions(
        logged_out_users=False,
        normal_users=True,
        admin_users=True,
        root_users=True))
def retrieve_specific(user_session: Optional[UserSession], token: str) -> Response:
    """ Method that returns a specific API client. Warning: this
        method only returns API clients that are enabled. """

    # Create a data object to return
    return_object = Response(success=False)

    if user_session is not None:
        try:
            # Get the API client from the database
            resources = get_api_clients(
                req_user=user_session.user,
                flt_token=token,
                flt_enabled=True
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


@blueprint_data_api_clients.route(
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
    """ Method to update clients. Should recieve the client id and the
        new data """

    # Get the given data
    post_data = request.json

    # Validate the given fields
    required_fields = {
        'client_id': validation_fields['client_id'],
    }

    # Set the optional fields
    optional_fields = {
        'app_name': validation_fields['app_name'],
        'app_publisher': validation_fields['app_publisher'],
        'redirect_url': validation_fields['redirect_url']
    }

    try:
        # Validate the user input
        validate_input(
            input_values=post_data,
            required_fields=required_fields,
            optional_fields=optional_fields)
    except IntegrityError as err:
        # Integrity errors happen mostly when the tag already
        # exists.
        raise ResourceIntegrityError(err)
    except (TypeError, FieldNotValidatedError) as e:
        raise InvalidInputError(e)

    # Delete `client_id` from the post_data dict. If we don't do this, we can't
    # use the `post_data` dict as input for the backend
    client_id = post_data['client_id']
    post_data.pop('client_id')

    # Create a data object to return
    return_object = Response(success=False)

    # Remove the resources
    if user_session is not None:
        try:
            # Get the tags from the database
            update_api_client(
                req_user=user_session.user,
                api_client_id=client_id,
                **post_data
            )

            # We create a key for the return object that will say that the data
            # is removed
            return_object.data = {'update': True}
        except NotFoundError as err:
            # If no clients are found, we set the data to False
            return_object.data = {'update': False}
        except Exception as err:
            # Every other error should result in a ServerError.
            raise ServerError(err)

        # Set the return value to True
        return_object.success = True

    # Return the created object
    return return_object


@blueprint_data_api_clients.route(
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
    """ Method to remove API clients. Should receive a list of ids to
        remove from the user in the POST data """

    # Get the given data
    post_data = request.json

    # Validate the given fields
    required_fields = {
        'api_client_ids': validation_fields['api_client_ids'],
    }

    # Set the optional fields
    optional_fields = None

    try:
        # Validate the user input
        validate_input(
            input_values=post_data,
            required_fields=required_fields,
            optional_fields=optional_fields)
    except IntegrityError as err:
        # Integrity errors happen mostly when the tag already
        # exists.
        raise ResourceIntegrityError(err)
    except (TypeError, FieldNotValidatedError) as e:
        raise InvalidInputError(e)

    # Create a data object to return
    return_object = Response(success=False)

    # Create dict to send to the my_database package
    data_dict = {
        'req_user': user_session.user,
        'api_client_id': post_data['api_client_ids']
    }

    # Remove the resources
    if user_session is not None:
        try:
            # Remove the API clients from the database
            delete_api_clients(**data_dict)

            # We create a key for the return object that will say that the data
            # is removed
            return_object.data = {'deleted': True}
        except NotFoundError as err:
            # If no API clients are found, we set the data to False
            return_object.data = {'deleted': False}
        except Exception as err:
            # Every other error should result in a ServerError.
            raise ServerError(err)

        # Set the return value to True
        return_object.success = True

    # Return the created object
    return return_object
