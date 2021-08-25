"""
    Module that contains the methods to get and set api token details
    from the database.
"""
from typing import List, Optional, Union
from database import DatabaseSession
from my_database_model import APIToken, User
from sqlalchemy.orm.query import Query
from my_database import logger
from my_database.exceptions import (FilterNotValidError, NotFoundError)


def get_api_tokens(
    req_user: Optional[User] = None,
    flt_id: Optional[int] = None,
    flt_token: Optional[str] = None
) -> Optional[Union[List[APIToken], APIToken]]:
    """ Method that retrieves all, or a subset of, the API tokens in
        the database.

        Parameters
        ----------
        req_user : Optional[User]
            The user who is requesting this. Should be used to verify
            what results the user gets. If this is not given, we assume
            this is a root user.

        flt_id : Optional[int]
            Filter on a specific token ID.

        flt_token : Optional[str]
            Filter on a specific token.

        Returns
        -------
        List[APIToken]
            A list with the resulting API tokens.

        APIToken
            The found API token (if filtered on a uniq value, like flt_id).

        None
            No API tokens are found.
    """

    # Empty data list
    data_list: Optional[Query] = None
    rv: Optional[List[APIToken]] = None

    if req_user is None:
        logger.warning('get_api_tokens: no user given. This should only be ' +
                       'done to authenticate API requests!')

    # Get the resources
    with DatabaseSession(commit_on_end=False, expire_on_commit=False) \
            as session:
        # First, we get all API tokens
        data_list = session.query(APIToken)
        logger.debug('get_api_tokens: we have the global list of API tokens')

        # If a user is given, we filter on the specific API tokens for
        # that user
        if req_user:
            data_list = data_list.filter(APIToken.user == req_user)
            logger.debug('get_api_tokens: filtered the tokens for this ' +
                         'specific user')

        # Now, we can apply the correct filters
        try:
            if flt_id:
                flt_id = int(flt_id)
                data_list = data_list.filter(APIToken.id == flt_id)
                logger.debug(
                    f'get_api_tokens: list is filtered on id {flt_id}')
        except (ValueError, TypeError):
            logger.error(
                f'API token id should be of type {int}, not {type(flt_id)}.')
            raise FilterNotValidError(
                f'API token id should be of type {int}, not {type(flt_id)}.')

        try:
            if flt_token:
                flt_token = str(flt_token)
                data_list = data_list.filter(APIToken.token == flt_token)
                logger.debug('get_api_tokens: list is filtered on token')
        except (ValueError, TypeError):
            logger.error(
                f'API token should be of type {str}, not {type(flt_id)}.')
            raise FilterNotValidError(
                f'API token should be of type {str}, not {type(flt_id)}.')

        # Get the data
        if flt_id or flt_token:
            rv = data_list.first()
            if rv is None:
                raise NotFoundError(
                    f'API token is not found.')
        else:
            rv = data_list.all()
            if len(rv) == 0:
                logger.debug('get_api_tokens: no API tokens to return')
                rv = None

    # Return the data
    logger.debug('get_api_tokens: returning API token')
    return rv
