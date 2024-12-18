""" Module that contains a function to verify if a user is logged in,
    and return it's user object """

from typing import Optional

from flask.globals import session

from my_database.exceptions import NotFoundError
from my_database.user_sessions import get_user_sessions
from my_database_model import UserSession


def get_active_user_session() -> Optional[UserSession]:
    """ Method to check if the Flask Session contains valid information
        for a user session and returns the UserSession Object for the
        session.

        Parameters
        ----------
        None

        Returns
        -------
        UserSession
            The UserSession object for the session.

        None
            There is no (valid) user session found in the Flask
            Session.
    """

    # Get the Flask Session
    if 'secret' in session.keys() and 'sid' in session.keys():
        # There is a existing session; check if this is valid
        try:
            session_object = get_user_sessions(
                req_user=None, flt_id=session['sid'])
        except NotFoundError:
            # Session was not found
            session.clear()
            return None

        # Session is found, let's compare secrets
        if session_object.secret != session['secret']:
            # Secret is not correct
            session.clear()
            return None

        # Everything looks fine; the session exists and has the same
        # secret as the user in it's Flask Session. Return the User
        # object for this session
        return session_object

    # The session was not valid; clear the session and return None
    session.clear()
    return None
