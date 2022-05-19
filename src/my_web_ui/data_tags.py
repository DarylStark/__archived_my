""" Module that creates the Flask Blueprint for the Tags data
    of the My Web UI service. This Blueprint can be used to get
    and manage Tags.
"""

from json import dumps
from typing import Optional
from flask.blueprints import Blueprint
from flask.globals import request, session
from my_database import validate_input
from my_database.tags import (get_tags)
from my_database.exceptions import (AuthCredentialsError,
                                    AuthUserRequiresSecondFactorError,
                                    FieldNotValidatedError, NotFoundError)
from my_database_model import User, UserSession, Tag
from my_web_ui.data_endpoint import EndpointPermissions, data_endpoint
from my_web_ui.exceptions import InvalidInputError, ServerError
from my_web_ui.response import Response

# Create the Blueprint
blueprint_data_tags = Blueprint(
    name='my_web_ui_data_tags',
    import_name=__name__,
    url_prefix='/data/tags/'
)


# TODO: ADD

@blueprint_data_tags.route(
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
    """ Method that returns all the tags for the logged on user """

    # Create a data object to return
    return_object = Response(success=False)

    if user_session is not None:
        try:
            # Get the tags from the database
            resources = get_tags(
                req_user=user_session.user
            )

            # Set the user session in the return object
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
