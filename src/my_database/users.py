"""
    Module that contains the methods to get user details from the
    database.
"""
# ---------------------------------------------------------------------
# Imports
from typing import List, Optional, Type

from sqlalchemy.orm.query import Query
from database import DatabaseSession
from my_database_model import User, UserRole
from my_database import logger
from my_database.exceptions import FilterNotValidError
# ---------------------------------------------------------------------
# Methods


def get_users(
    req_user: User,
    flt_id: Optional[int] = None
) -> Optional[List[User]]:
    """ Method that retrieves all, or a subset of, the users in the
        database.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what results the user gets.

        flt_id : Optional[int]
            Filter on a specific user ID.

        Returns
        -------
        List[User]
            A list with the resulting users.

        None
            No users are found.
    """

    # Empty data list
    data_list: Optional[Query] = None

    # Get the token
    with DatabaseSession(commit_on_end=False, expire_on_commit=False) \
            as session:
        # First, we get all users
        data_list = session.query(User)

        # Then, we check the role that this user has. 'Root' users can
        # retrieve all users. Admin users can retrieve
        role = req_user.role

        if role == UserRole.admin:
            # Admin role: only sees other admins and other users
            data_list = data_list.filter(User.role != UserRole.root)
        elif role == UserRole.user:
            # Normal user: only sees it's own profile
            data_list = data_list.filter(User.id == req_user.id)

        # Now, we can apply the correct filters
        try:
            if flt_id:
                flt_id = int(flt_id)
                data_list = data_list.filter(User.id == flt_id)
        except (ValueError, TypeError):
            logger.error(
                f'User id should be of type {int}, not {type(flt_id)}.')
            raise FilterNotValidError(
                f'User id should be of type {int}, not {type(flt_id)}.')

    # Return the token
    if data_list is not None:
        return data_list.all()
    return None
# ---------------------------------------------------------------------
