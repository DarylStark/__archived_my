"""
    Module that has the authorization function. This function will be
    used by the REST API to authorize API requests.
"""
import logging
from typing import List, Optional, Union
from my_database.api_authorization import get_token_information
from rest_api_generator.authorization import Authorization
from rest_api_generator.rest_api_generator import (BasicAuthorization,
                                                   BearerAuthorzation)


def authorization(
        auth: Optional[Union[BasicAuthorization, BearerAuthorzation]],
        scopes: Optional[List[str]]) -> Authorization:
    """
        Method that does the authentication for the REST API.

        Parameters
        ----------
        auth : Optional[Union[BasicAuthorization, BearerAuthorzation]]
            The authentication header from the Flask Request. Can be
            None, a BasicAuthorization object or a BearerAuthorization
            object, depending on the given authorization.

        scopes : Optional[List[str]]
            The scopes that are defined in the endpoint that are
            required for this endpoint.

        Returns
        -------
        RESTAPIAuthorization:
            A object containing the authorization information.
    """

    # Create a logger
    logger = logging.getLogger('api_authorization')

    # Create a authorization object
    auth_object: Authorization = Authorization()

    if type(scopes) is list:
        logger.debug(
            f'Authorizing request started. Scopes: {",".join(scopes)}')

    # Check the type of authorization we received. We only accept the
    # 'Bearer' kind, since that is being used in OAuth world.
    if type(auth) is not BearerAuthorzation:
        logger.error(f'Auth is of type {type(auth)}, not BearerAuthorization')
        return auth_object

    # Get the token object
    token_object = get_token_information(auth.token)

    # If we didn't get a object, the token is wrong
    if token_object is None:
        logger.error('Got no token object; authorization failed')
        auth_object.authorized = False
        return auth_object

    # Get the associated scopes
    token_scopes = [
        token_scope.scope.full_scope_name
        for token_scope in token_object.token_scopes
    ]

    # Check if any of the given scopes is in the 'token scopes'
    for scope in scopes:
        if scope in token_scopes:
            logger.debug(f'Found scope {scope} in token_scopes! Authorized!')
            auth_object.authorized = True
            auth_object.data = token_object
            break

    # Return authorization object
    if not auth_object.authorized:
        logger.error('Not authorized')
    return auth_object
