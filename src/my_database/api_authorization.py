"""
    Module that contains the methods to get API authentication details
    from the database.
"""
# ---------------------------------------------------------------------
# Imports
from typing import Optional
from database import DatabaseSession
from my_database_model import APIToken
from my_database_model.api_token_scope import APITokenScope
# ---------------------------------------------------------------------
# Methods


def get_token_information(token: str) -> Optional[APIToken]:
    """ Method that retrieves token information by a specific token.
        Can be used by the REST API authentication method to verify if
        a request is authorized.

        Parameters
        ----------
        token : str
            The token to verify

        Returns
        -------
        APIToken
            The API token object from the database.

        None
            If no token is found.
    """

    # Set an empty token_object
    token_object: Optional[APIToken] = None

    # Get the token
    with DatabaseSession(commit_on_end=False, expire_on_commit=False) as session:
        token_object = session.query(APIToken).filter(
            APIToken.token == token
        ).first()

    # Return the token
    return token_object
# ---------------------------------------------------------------------
