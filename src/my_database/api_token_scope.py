""" Module that contas the function to get and remove API token Scopes """


from typing import List, Optional, Union
from my_database.field import Field
import sqlalchemy
from database import DatabaseSession
from my_database import validate_input
from my_database_model import APIToken, User, APITokenScope
from sqlalchemy.orm.query import Query
from my_database import logger
from datetime import datetime
from my_database.exceptions import (FilterNotValidError,
                                    IntegrityError, NotFoundError)
from my_database.api_scopes import get_scopes
from my_database_model.api_scope import APIScope


def get_api_token_scopes(
    req_user: Optional[User] = None,
    flt_id: Optional[int] = None
) -> Optional[Union[List[APITokenScope], APITokenScope]]:
    """ Method that retrieves all, or a subset of, the API token scopes in
        the database.

        Parameters
        ----------
        req_user : Optional[User]
            The user who is requesting this. Should be used to verify
            what results the user gets. If this is not given, we assume
            this is a root user.

        flt_id : Optional[int] [default=None]
            Filter on a specific token ID.

        Returns
        -------
        List[APITokenScope]
            A list with the resulting API tokens scopes

        APITokenScope
            The found API token scope (if filtered on a uniq value, like flt_id).

        None
            No API tokens are found.
    """

    # Empty data list
    data_list: Optional[Query] = None
    rv: Optional[List[APIToken]] = None

    if req_user is None:
        logger.warning('get_api_token_scopes: no user given. This should only be ' +
                       'done to authenticate API requests!')

    # Get the resources
    with DatabaseSession(commit_on_end=False, expire_on_commit=False) \
            as session:
        # First, we get all API tokens
        data_list = session.query(APITokenScope)
        logger.debug(
            'get_api_token_scopes: we have the global list of API tokens')

        # If a user is given, we filter on the specific API tokens for
        # that user
        if req_user:
            data_list = data_list.filter(APIToken.user == req_user)
            logger.debug('get_api_token_scopes: filtered the tokens for this ' +
                         'specific user')

        # Now, we can apply the correct filters
        try:
            if flt_id:
                flt_id = int(flt_id)
                data_list = data_list.filter(APITokenScope.id == flt_id)
                logger.debug(
                    f'get_api_token_scopes: list is filtered on id {flt_id}')
        except (ValueError, TypeError):
            logger.error(
                f'API token id should be of type {int}, not {type(flt_id)}.')
            raise FilterNotValidError(
                f'API token id should be of type {int}, not {type(flt_id)}.') from None

        # Get the data
        if flt_id:
            rv = data_list.first()
            if rv is None:
                raise NotFoundError(
                    f'API token is not found.')
        else:
            rv = data_list.all()
            if len(rv) == 0:
                logger.debug('get_api_token_scopes: no API tokens to return')
                rv = None

    # Return the data
    logger.debug('get_api_token_scopes: returning API token')
    return rv


def delete_api_token_scopes(
    req_user: User,
    token_scope_ids: Union[List[int], int]
) -> bool:
    """ Method to delete a API token scope.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what the user is allowed to do.

        token_scope_ids : int
            The IDs for the API token scopes to delete.

        Returns
        -------
        bool
            True on success.
    """

    # Get the API token
    resources = None
    if type(token_scope_ids) is list:
        resources = [
            get_api_token_scopes(req_user=req_user, flt_id=r)
            for r in token_scope_ids
        ]
    else:
        resources = [get_api_token_scopes(
            req_user=req_user, flt_id=token_scope_ids)]

    logger.debug('delete_api_token_scopes: we have the resources')

    # Create a database session
    try:
        with DatabaseSession(
            commit_on_end=True,
            expire_on_commit=True
        ) as session:
            # Delete the resource
            logger.debug('delete_api_token_scopes: deleting the resource')
            for resource in resources:
                session.delete(resource)
    except sqlalchemy.exc.IntegrityError as sa_error:
        logger.error(
            f'def delete_api_token_scopes: sqlalchemy.exc.IntegrityError: {str(sa_error)}')
        raise IntegrityError(
            'API token couldn\'t be deleted because it still has resources ' +
            'connected to it') from sa_error
    else:
        logger.debug(
            'def delete_api_token_scopes: return True because it was a success')
        return True
