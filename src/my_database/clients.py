"""
    Module that contains the methods to get client details from the
    database.
"""
from typing import List, Optional
from database import DatabaseSession
from my_database.generic import delete_object
from my_database.tokens import delete_token
from my_database_model import User, APIToken
from sqlalchemy.orm.query import Query
from my_database import logger
from my_database.exceptions import FilterNotValidError, IntegrityError, ResourceNotFoundError
from my_database_model.api_client import APIClient


def get_api_clients(
    req_user: Optional[User],
    flt_id: Optional[int] = None
) -> Optional[List[APIClient]]:
    """ Method that retrieves all, or a subset of, the clients in the
        database.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what results the user gets. If this is set to 'None',
            we bypass this check.

        flt_id : Optional[int]
            Filter on a specific client ID.

        Returns
        -------
        List[APIClient]
            A list with the resulting clients.

        None
            No clients are found.
    """

    # Empty data list
    data_list: Optional[Query] = None
    rv: Optional[List[APIClient]] = None

    # Get the token
    with DatabaseSession(commit_on_end=False, expire_on_commit=False) \
            as session:
        # First, we get all token
        data_list = session.query(APIClient)

        # If a user is specified, we use that user to filter the
        # clients
        if req_user:
            data_list = data_list.filter(APIClient.user_id == req_user.id)

        # Now, we can apply the correct filters
        try:
            if flt_id:
                flt_id = int(flt_id)
                data_list = data_list.filter(APIClient.id == flt_id)
        except (ValueError, TypeError):
            logger.error(
                f'Client id should be of type {int}, not {type(flt_id)}.')
            raise FilterNotValidError(
                f'Client id should be of type {int}, not {type(flt_id)}.')

        # Get the data
        if data_list is not None:
            rv = data_list.all()

    # Return the data
    return rv


def delete_api_client(
    req_user: Optional[User],
    client_id: int
) -> bool:
    """ Method to delete a API client.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what the user is allowed to do.

        client_id : int
            The ID for the API client to delete.

        Returns
        -------
        bool
            True on success.
    """

    # Get the resource object
    resource: Optional[List[APIClient]] = get_api_clients(
        req_user,
        flt_id=client_id)

    # Check if we got a resource. If we didn't, we rise an error
    # indicating that the resource wasn't found. This can be either
    # because it didn't exist, or because the user has no permissions
    # to it.
    if resource is None or len(resource) == 0:
        raise ResourceNotFoundError(
            f'Client with ID {client_id} is not found.')

    # Appearently we have resources. Because the result is a list, we
    # we can assume the first one in the list is the one we are
    # interested in.
    resource = resource[0]

    # Delete the resource
    try:
        # Before we can delete the resource, we have to get the
        # resources that are connected to this resource.
        # Delete all connected tokens
        for connected_resource in [rs for rs in resource.tokens]:
            # Remove the connected resource
            delete_token(
                req_user=None,
                token_id=connected_resource.id)

            # Remove it from the resource
            resource.tokens.remove(connected_resource)

        # Delete the resource itself
        delete_object(resource)
    except IntegrityError:
        # Add a custom text to the exception
        raise IntegrityError(
            'Token couldn\'t be deleted because it still has resources ' +
            'connected to it')
    else:
        return resource
