""" Module that creates the Flask Blueprint for the Tags data
    of the My Web UI service. This Blueprint can be used to get
    and manage Tags.
"""

from json import dumps
from typing import Optional
from flask.blueprints import Blueprint
from flask.globals import request, session
from my_database import validate_input
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
blueprint_data_tags = Blueprint(
    name='my_web_ui_data_tags',
    import_name=__name__,
    url_prefix='/data/tags/'
)


@blueprint_data_tags.route(
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
    """ Method to create tags. Should recieve the session id and the
        new data """

    # Get the given data
    post_data = request.json

    # Validate the given fields
    required_fields = {
        'title': validation_fields['title']
    }

    # Set the optional fields
    optional_fields = {
        'color': validation_fields['color']
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
            new_object = create_tag(
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

    # Return the created object
    return return_object


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


@blueprint_data_tags.route(
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
    """ Method to update tags. Should recieve the tag id and the
        new data """

    # Get the given data
    post_data = request.json

    # Validate the given fields
    required_fields = {
        'tag_id': validation_fields['tag_id'],
    }

    # Set the optional fields
    optional_fields = {
        'title': validation_fields['title'],
        'color': validation_fields['color']
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

    # Delete `tag_id` from the post_data dict. If we don't do this, we can't
    # use the `post_data` dict as input for the backend
    tag_id = post_data['tag_id']
    post_data.pop('tag_id')

    # Create a data object to return
    return_object = Response(success=False)

    # Remove the resources
    if user_session is not None:
        try:
            # Get the tags from the database
            update_tag(
                req_user=user_session.user,
                tag_id=tag_id,
                **post_data
            )

            # We create a key for the return object that will say that the data
            # is removed
            return_object.data = {'update': True}
        except NotFoundError as err:
            # If no tags are found, we set the data to False
            return_object.data = {'update': False}
        except Exception as err:
            # Every other error should result in a ServerError.
            raise ServerError(err)

        # Set the return value to True
        return_object.success = True

    # Return the created object
    return return_object


@blueprint_data_tags.route(
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
    """ Method to remove tags. Should receive a list of ids to
        remove from the user in the POST data """

    # Get the given data
    post_data = request.json

    # Validate the given fields
    required_fields = {
        'tag_ids': validation_fields['tag_ids'],
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
        'tag_id': post_data['tag_ids']
    }

    # Remove the resources
    if user_session is not None:
        try:
            # Remove the tags from the database
            delete_tags(**data_dict)

            # We create a key for the return object that will say that the data
            # is removed
            return_object.data = {'deleted': True}
        except NotFoundError as err:
            # If no tags are found, we set the data to False
            return_object.data = {'deleted': False}
        except Exception as err:
            # Every other error should result in a ServerError.
            raise ServerError(err)

        # Set the return value to True
        return_object.success = True

    # Return the created object
    return return_object
