""" Module that creates the Flask Blueprint for the Dashboard data
    of the My Web UI service. This Blueprint can be used to get
    and manage dashboard elements, like tags.
"""

from json import dumps
from typing import Optional
from flask.blueprints import Blueprint
from flask.globals import request, session
from my_database import validate_input
from my_database.date_tags import (
    delete_date_tags, get_date_tags, validation_fields, create_date_tag)
from my_database.exceptions import (AuthCredentialsError,
                                    AuthUserRequiresSecondFactorError,
                                    FieldNotValidatedError, IntegrityError, NotFoundError)
from my_database_model import User, UserSession, Tag
from my_web_ui.data_endpoint import EndpointPermissions, data_endpoint
from my_web_ui.exceptions import InvalidInputError, ResourceIntegrityError, ResourceNotFoundError, ServerError
from my_web_ui.response import Response

# Create the Blueprint
blueprint_data_dashboard = Blueprint(
    name='my_web_ui_data_dashboard',
    import_name=__name__,
    url_prefix='/data/dashboard/'
)


@blueprint_data_dashboard.route(
    '/tag',
    methods=['POST', 'DELETE']
)
@data_endpoint(
    allowed_users=EndpointPermissions(
        logged_out_users=False,
        normal_users=True,
        admin_users=True,
        root_users=True))
def tag(user_session: Optional[UserSession]) -> Response:
    """ Method to tag or untag a specific date. Should recieve the tag ID and
        the date to tag or untag """

    # Get the given data
    post_data = request.json

    # Validate the given fields
    required_fields = {
        'date': validation_fields['date'],
        'tag_id': validation_fields['tag_id']
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

    # Add the resources
    if request.method == 'POST':
        if user_session is not None:
            try:
                # Create the tag
                new_object = create_date_tag(
                    req_user=user_session.user,
                    **post_data
                )

                # Set the tag in the object
                return_object.data = new_object
                return_object.success = True
            except IntegrityError as err:
                # Integrity errors happen mostly when the tag already
                # exists.
                raise ResourceIntegrityError(err)
            except Exception as err:
                # Every other error should result in a ServerError.
                raise ServerError(err)

    # Delete the resource
    if request.method == 'DELETE':
        if user_session is not None:
            try:
                # Retrieve the tag
                resource = get_date_tags(
                    req_user=user_session.user,
                    flt_date=post_data['date'],
                    flt_tag_id=post_data['tag_id']
                )

                if resource is None:
                    raise ResourceNotFoundError

                # Delete the tag
                new_object = delete_date_tags(
                    req_user=user_session.user,
                    date_tag_ids=resource[0].id
                )

                # Set the tag in the object
                return_object.data = new_object
                return_object.success = True
            except IntegrityError as err:
                # Integrity errors happen mostly when the tag already
                # exists.
                raise ResourceIntegrityError(err)
            except ResourceNotFoundError as err:
                raise ResourceNotFoundError(err)
            except Exception as err:
                # Every other error should result in a ServerError.
                raise ServerError(err)

    # Return the created object
    return return_object


@blueprint_data_dashboard.route(
    'tags/<string:date>',
    methods=['GET']
)
@data_endpoint(
    allowed_users=EndpointPermissions(
        logged_out_users=False,
        normal_users=True,
        admin_users=True,
        root_users=True))
def tags(user_session: Optional[UserSession], date: str) -> Response:
    """ Method that returns all the tags for the specified date """

    # Create a data object to return
    return_object = Response(success=False)

    if user_session is not None:
        try:
            # Get the tags from the database
            resources = get_date_tags(
                req_user=user_session.user,
                flt_date=date
            )

            # Set the tags in the return object
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
