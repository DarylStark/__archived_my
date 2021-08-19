"""
    Module that contains the methods to get tag details from the
    database.
"""
from typing import List, Optional
from database import DatabaseSession
from my_database_model import User, Tag
from sqlalchemy.orm.query import Query
from my_database import logger
from my_database.exceptions import FilterNotValidError


def get_tags(
    req_user: User,
    flt_id: Optional[int] = None
) -> Optional[List[Tag]]:
    """ Method that retrieves all, or a subset of, the tags in the
        database.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what results the user gets.

        flt_id : Optional[int]
            Filter on a specific tag ID.

        Returns
        -------
        List[User]
            A list with the resulting tags.

        None
            No users are found.
    """

    # Empty data list
    data_list: Optional[Query] = None
    rv: Optional[List[Tag]] = None

    # Get the token
    with DatabaseSession(commit_on_end=False, expire_on_commit=False) \
            as session:
        # First, we get all tags for the specified user
        data_list = session.query(Tag).filter(Tag.user_id == req_user.id)

        # Now, we can apply the correct filters
        try:
            if flt_id:
                flt_id = int(flt_id)
                data_list = data_list.filter(Tag.id == flt_id)
        except (ValueError, TypeError):
            logger.error(
                f'Tag id should be of type {int}, not {type(flt_id)}.')
            raise FilterNotValidError(
                f'Tag id should be of type {int}, not {type(flt_id)}.')

        # Get the data
        if data_list is not None:
            rv = data_list.all()

    # Return the data
    return rv
