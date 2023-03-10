""" Module that contains a decorator that can be used for the 'data'
    functions. This decorator will make sure the result gets formatted
    correctly and will make sure the user is logged in (if needed). """

from dataclasses import dataclass
from json import dumps
from typing import Callable, Optional

from flask.app import Response as FlaskResponse

from my_database_model.user import UserRole
from my_web_ui.authentication import get_active_user_session
from my_web_ui.exceptions import (InvalidInputError, PermissionDeniedError,
                                  ResourceIntegrityError,
                                  ResourceNotFoundError, ServerError)
from my_web_ui.json_encoder import WebUIJSONEncoder
from my_web_ui.response import Response


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

        def endpoint(**kwargs) -> FlaskResponse:
            """ The function that will be used instead of the normal
                function. """

            # Get the logged in user
            user_session = get_active_user_session()
            user_object = None
            if user_session is not None:
                user_object = user_session.user

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
                    response = func(user_session, **kwargs)
                except InvalidInputError:
                    # User supplied invalid input
                    status_code = 400
                except PermissionDeniedError:
                    # User did something without permissions
                    status_code = 401
                except ResourceNotFoundError:
                    # Resource not found
                    status_code = 404
                except ResourceIntegrityError:
                    # Integrity error
                    status_code = 409
                except ServerError:
                    # Something went wrong on the server
                    status_code = 500

            # Return the Flask Response
            return FlaskResponse(
                response=dumps(
                    response,
                    cls=WebUIJSONEncoder),
                status=status_code,
                mimetype='application/json'
            )

        # Return the function. Before we do that, we update the name of
        # the method so Flask can use mulitple of it.
        endpoint.__name__ = func.__name__
        return endpoint

    # Return the decorator
    return decorator
