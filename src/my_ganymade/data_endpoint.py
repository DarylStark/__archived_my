""" Module that contains a decorator that can be used for the 'data'
    functions. This decorator will make sure the result gets formatted
    correctly and will make sure the user is logged in (if needed). """

from typing import Callable, Optional
from flask.app import Response as FlaskResponse
from my_database_model.user import UserRole
from my_ganymade.response import Response
from my_ganymade.json_encoder import GanymedeJSONEncoder
from json import dumps
from my_ganymade.exceptions import InvalidInputError
from my_ganymade.authentication import logged_in_user
from dataclasses import dataclass


@dataclass
class EndpointPermissions:
    """ Dataclass that specifies which types of users can use a
        specific endpoint.

        Members
        -------
        logged_out_users : bool [default=False]
            Specifies if users that are not authenticated can use this
            endpoint.

        normal_users : bool [default=False]
            Specifies if normal users can use this endpoint.

        admin_users : bool [default=False]
            Specifies if admin users can use this endpoint.

        root_users : bool [default=False]
            Specifies if root users can use this endpoint.
    """

    logged_out_users: bool = False
    normal_users: bool = False
    admin_users: bool = False
    root_users: bool = False


def data_endpoint(allowed_users: EndpointPermissions):
    """ Decorator that should be used for 'data' endpoints. """

    def decorator(func: Callable):
        """ The real decorator returns a function that is used instead
            of the normal function. """

        def endpoint() -> FlaskResponse:
            """ The function that will be used instead of the normal
                function. """

            # Get the logged in user
            user_object = logged_in_user()

            # For logged out users
            verified = False
            if user_object is None and allowed_users.logged_out_users:
                verified = True

            if user_object is not None:
                if (
                    (user_object.role == UserRole.user and
                     allowed_users.normal_users) or
                    (user_object.role == UserRole.admin and
                     allowed_users.admin_users) or
                    (user_object.role == UserRole.root and
                     allowed_users.root_users)
                ):
                    verified = True

            # Default values
            status_code: int = 200

            # Empty response
            response: Optional[Response] = Response(
                success=False
            )

            if not verified:
                status_code = 403
            else:
                # Get the response from the function
                try:
                    response = func()
                except InvalidInputError:
                    # User supplied invalid input
                    status_code = 400

            # Return the Flask Response
            return FlaskResponse(
                response=dumps(
                    response,
                    cls=GanymedeJSONEncoder),
                status=status_code,
                mimetype='application/json'
            )

        # Return the function
        return endpoint

    # Return the decorator
    return decorator
