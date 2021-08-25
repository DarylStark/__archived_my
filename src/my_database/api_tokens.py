"""
    Module that contains the methods to get and set api token details
    from the database. In contrast to other modules in the
    `my_database` package, this module doesn't contain a method to
    update API tokens. This is because a API token should not be
    updatable; it cannot be changed.
"""
from typing import List, Optional, Union
import sqlalchemy
from database import DatabaseSession
from my_database_model import APIToken, User
from sqlalchemy.orm.query import Query
from my_database import logger
from my_database.exceptions import (FilterNotValidError,
                                    IntegrityError, NotFoundError)


def create_api_token(req_user: User, **kwargs: dict) -> Optional[APIToken]:
    """" Method to create a API token

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what the user is allowed to do.

        **kwargs : dict
            A dict containing the fields for the API token.

        Returns
        -------
        APIToken
            The created API token object.

    """

    # Check if we have all fields
    needed_fields = [
        'client_id'
    ]
    for field in needed_fields:
        if field not in kwargs.keys():
            raise TypeError(
                f'Missing required argument "{field}"')

    logger.debug('create_api_token: all needed fields are given')

    # Set the optional fields
    optional_fields = list()

    # Check if no other fields are given
    possible_fields = needed_fields + optional_fields
    for field in kwargs.keys():
        if field not in possible_fields:
            raise TypeError(
                f'Unexpected field "{field}"')

    try:
        with DatabaseSession(
            commit_on_end=True,
            expire_on_commit=True
        ) as session:
            # Create the resource
            new_resource = APIToken(
                user=req_user,
                client_id=kwargs['client_id']
            )

            # Set token
            new_resource.generate_random_token()

            logger.debug('create_api_token: adding API token')

            # Add the resource
            session.add(new_resource)

            # Return the created resource
            return new_resource
    except sqlalchemy.exc.IntegrityError as e:
        logger.error(f'create_api_token: IntegrityError: {str(e)}')
        # Add a custom text to the exception
        raise IntegrityError('API token already exists')

    return None


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


def delete_api_token(
    req_user: User,
    api_token_id: int
) -> bool:
    """ Method to delete a API token.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what the user is allowed to do.

        api_token_id : int
            The ID for the API token to delete.

        Returns
        -------
        bool
            True on success.
    """

    # Get the API token
    resource = get_api_tokens(req_user=req_user, flt_id=api_token_id)

    logger.debug('delete_api_token: we have the resource')

    # Create a database session
    try:
        with DatabaseSession(
            commit_on_end=True,
            expire_on_commit=True
        ) as session:
            # Delete the resource
            logger.debug('delete_api_token: deleting the resource')
            session.delete(resource)
    except sqlalchemy.exc.IntegrityError as e:
        logger.error(
            f'delete_api_token: sqlalchemy.exc.IntegrityError: {str(e)}')
        raise IntegrityError(
            'API token couldn\'t be deleted because it still has resources ' +
            'connected to it')
    else:
        logger.debug('delete_api_token: return True because it was a success')
        return True
