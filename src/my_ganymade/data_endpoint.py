""" Module that contains a decorator that can be used for the 'data'
    functions. This decorator will make sure the result gets formatted
    correctly and will make sure the user is logged in (if needed). """

from typing import Callable, Optional
from flask.app import Response as FlaskResponse
from my_ganymade.response import Response
from my_ganymade.json_encoder import GanymedeJSONEncoder
from json import dumps


def data_endpoint(allowed_users: Optional[list] = None):
    """ Decorator that should be used for 'data' endpoints. """

    def decorator(func: Callable):
        """ The real decorator returns a function that is used instead
            of the normal function. """

        def endpoint() -> FlaskResponse:
            """ The function that will be used instead of the normal
                function. """

            # TODO: Check the 'allowed_users' lists

            # Default values
            status_code: int = 200

            # Get the response from the function
            try:
                response: Response = func()
            except:
                # Generic error; we don't know what went wrong
                status_code = 500

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
