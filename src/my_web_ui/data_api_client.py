""" Module that creates the Flask Blueprint for the API client data
    of the My Web UI service. This Blueprint can be used to get
    configured API clients
"""

from json import dumps
from typing import Optional
from flask.blueprints import Blueprint
from flask.globals import request, session
from my_database import validate_input
from my_database.api_clients import get_api_clients
from my_database.tags import (
    create_tag, delete_tags, get_tags, update_tag, validation_fields)
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
    """ Method that returns a specific API client """

    # Create a data object to return
    return_object = Response(success=False)

    # Get the given data
    url_data = request.args

    if user_session is not None:
        try:
            # Get the API client from the database
            resources = get_api_clients(
                req_user=user_session.user,
                flt_id=url_data.get('id', None) if url_data.get(
                    'id', None) is None else int(url_data.get('id', None)),
                flt_token=url_data.get('token', None)
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
