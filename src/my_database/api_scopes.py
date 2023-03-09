""" Module that contains the methods to get API scope details from
    the database. """

from typing import List, Optional, Union
import sqlalchemy
from sqlalchemy.orm.query import Query
from database import DatabaseSession
from my_database import validate_input
from my_database.field import Field
from my_database_model import APIScope, User
from my_database import logger
from my_database.exceptions import (FilterNotValidError, IntegrityError,
                                    NotFoundError)
from my_database.exceptions import (FilterNotValidError,
                                    IntegrityError, NotFoundError)


def get_scopes(
    req_user: User,
    flt_id: Optional[int] = None,
    flt_module: Optional[str] = None,
    flt_subject: Optional[str] = None
) -> Optional[Union[List[APIScope], APIScope]]:
    """ Method that retrieves all, or a subset of, the scopes in the
        database.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what results the user gets.

        flt_id : Optional[int] [default=None]
            Filter on a specific ID

        flt_module : Optional[str] [default=None]
            Filter on a specific module

        flt_subject : Optional[str] [default=None]
            Filter on a specific subject

        Returns
        -------
        List[Scope]
            A list with the resulting scopes.

        Scope
            The found scope (if filtered on a uniq value, like flt_id).

        None
            No scopes are found.
    """

    # Empty data list
    data_list: Optional[Query] = None
    rv: Optional[List[APIScope]] = None

    # Get the resources
    with DatabaseSession(commit_on_end=False, expire_on_commit=False) \
            as session:

        # First, we get all scopes
        data_list = session.query(APIScope)

        logger.debug('get_scopes: we have the global list of scopes')

        # Apply filter for ID
        try:
            if flt_id:
                flt_id = int(flt_id)
                data_list = data_list.filter(APIScope.id == flt_id)
                logger.debug('get_scopes: list is filtered on ID')
        except (ValueError, TypeError):
            logger.error(
                f'APIScope id should be of type {int}, not {type(flt_id)}.')
            raise FilterNotValidError(
                f'APIScope id should be of type {int}, not {type(flt_id)}.') from None

        # Apply filter for module
        try:
            if flt_module:
                flt_module = str(flt_module)
                data_list = data_list.filter(APIScope.module == flt_module)
                logger.debug('get_scopes: list is filtered on module')
        except (ValueError, TypeError):
            logger.error(
                f'APIScope module should be of type {str}, not {type(flt_module)}.')
            raise FilterNotValidError(
                f'APIScope module should be of type {str}, not {type(flt_module)}.') from None

        # Apply filter for subject
        try:
            if flt_subject:
                flt_subject = str(flt_subject)
                data_list = data_list.filter(APIScope.subject == flt_subject)
                logger.debug('get_scopes: list is filtered on subject')
        except (ValueError, TypeError):
            logger.error(
                f'APIScope subject should be of type {str}, not {type(flt_subject)}.')
            raise FilterNotValidError(
                f'APIScope subject should be of type {str}, not {type(flt_subject)}.') from None

        # Get the data
        if flt_id:
            rv = data_list.first()
            if rv is None:
                raise NotFoundError(
                    f'APIScope with ID {flt_id} is not found.')
        else:
            rv = data_list.all()
            if len(rv) == 0:
                logger.debug('get_scopes: no scopes to return')
                rv = None

    # Return the data
    logger.debug('get_scopes: returning scopes')
    return rv
