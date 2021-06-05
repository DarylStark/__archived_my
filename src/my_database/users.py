"""
    Module that contains the methods to get user details from the
    database.
"""
# ---------------------------------------------------------------------
# Imports
from typing import List, Optional
from database import DatabaseSession
from my_database_model import User, UserRole
# ---------------------------------------------------------------------
# Methods


def get_users(req_user: User) -> Optional[List[User]]:
    """ Method that retrieves all, or a subset of, the users in the
        database.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what results the user gets.

        Returns
        -------
        List[User]
            A list with the resulting users.

        None
            No users are found.
    """

    # Empty data list
    data_list = None

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

    # Return the token
    return data_list.all()
# ---------------------------------------------------------------------
