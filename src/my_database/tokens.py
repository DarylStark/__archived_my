"""
    Module that contains the methods to get token details from the
    database.
"""
from typing import List, Optional
from database import DatabaseSession
from my_database.generic import delete_object
from my_database_model import User, APIToken
from sqlalchemy.orm.query import Query
from my_database import logger
from my_database.exceptions import FilterNotValidError, IntegrityError, ResourceNotFoundError


def get_tokens(
    req_user: Optional[User],
    flt_id: Optional[int] = None
) -> Optional[List[APIToken]]:
    """ Method that retrieves all, or a subset of, the tokens in the
        database.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what results the user gets. If this is set to 'None',
            we bypass this check.

        flt_id : Optional[int]
            Filter on a specific token ID.

        Returns
        -------
        List[APIToken]
            A list with the resulting tokens.

        None
            No tokens are found.
    """

    # Empty data list
    data_list: Optional[Query] = None
    rv: Optional[List[APIToken]] = None

    # Get the token
    with DatabaseSession(commit_on_end=False, expire_on_commit=False) \
            as session:
        # First, we get all token
        data_list = session.query(APIToken)

        # If a user is specified, we use that user to filter the tokens
        if req_user:
            data_list = data_list.filter(APIToken.user_id == req_user.id)

        # Now, we can apply the correct filters
        try:
            if flt_id:
                flt_id = int(flt_id)
                data_list = data_list.filter(APIToken.id == flt_id)
        except (ValueError, TypeError):
            logger.error(
                f'Token id should be of type {int}, not {type(flt_id)}.')
            raise FilterNotValidError(
                f'Token id should be of type {int}, not {type(flt_id)}.')

        # Get the data
        if data_list is not None:
            rv = data_list.all()

    # Return the data
    return rv


def delete_token(
    req_user: Optional[User],
    token_id: int
) -> Optional[APIToken]:
    """ Method to delete a token.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what the user is allowed to do.

        token_id : int
            The ID for the token to delete.

        Returns
        -------
        bool
            True on success.
    """

    # Get the resource object
    resource: Optional[List[APIToken]] = get_tokens(req_user, flt_id=token_id)

    # Check if we got a resource. If we didn't, we rise an error
    # indicating that the resource wasn't found. This can be either
    # because it didn't exist, or because the user has no permissions
    # to it.
    if resource is None or len(resource) == 0:
        raise ResourceNotFoundError(f'Token with ID {token_id} is not found.')

    # Appearently we have resources. Because the result is a list, we
    # we can assume the first one in the list is the one we are
    # interested in.
    resource = resource[0]

    # Delete the resource
    try:
        # Before we can delete the resource, we have to get the
        # resources that are connected to this resource.
        # Delete all connected token_scopes
        for connected_resource in [rs for rs in resource.token_scopes]:
            # Remove the connected resource
            # TODO: Create a seperate `my_database` module or function
            #       for this
            delete_object(connected_resource)

            # Remove it from the resource
            resource.token_scopes.remove(connected_resource)

        # Delete the resource itself
        delete_object(resource)
    except IntegrityError:
        # Add a custom text to the exception
        raise IntegrityError(
            'Token couldn\'t be deleted because it still has resources ' +
            'connected to it')
    else:
        return resource
