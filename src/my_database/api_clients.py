"""
    Module that contains the methods to get and set api client details
    from the database.
"""
from typing import List, Optional, Union
import sqlalchemy
from database import DatabaseSession
from my_database_model import APIClient, User
from sqlalchemy.orm.query import Query
from my_database import logger
from my_database.exceptions import (FilterNotValidError,
                                    IntegrityError, NotFoundError)


def create_api_client(req_user: User, **kwargs: dict) -> Optional[APIClient]:
    """" Method to create a API client

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what the user is allowed to do.

        **kwargs : dict
            A dict containing the fields for the API client.

        Returns
        -------
        APIClient
            The created API client object.

    """

    # Check if we have all fields
    needed_fields = [
        'app_name', 'app_publisher'
    ]
    for field in needed_fields:
        if field not in kwargs.keys():
            raise TypeError(
                f'Missing required argument "{field}"')

    logger.debug('create_api_client: all needed fields are given')

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
            new_resource = APIClient(
                app_name=kwargs['app_name'],
                app_publisher=kwargs['app_publisher'],
                user=req_user
            )

            # Set token
            new_resource.generate_random_token()

            logger.debug('create_api_client: adding API client')

            # Add the resource
            session.add(new_resource)

            # Return the created resource
            return new_resource
    except sqlalchemy.exc.IntegrityError as e:
        logger.error(f'create_user: IntegrityError: {str(e)}')
        # Add a custom text to the exception
        raise IntegrityError('API client already exists')

    return None


def get_api_clients(
    req_user: User,
    flt_id: Optional[int] = None
) -> Optional[Union[List[APIClient], APIClient]]:
    """ Method that retrieves all, or a subset of, the API clients in
        the database.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what results the user gets.

        flt_id : Optional[int]
            Filter on a specific client ID.

        Returns
        -------
        List[APIClient]
            A list with the resulting API clients.

        APIClient
            The found API client (if filtered on a uniq value, like
            flt_id).

        None
            No API clients are found.
    """

    # Empty data list
    data_list: Optional[Query] = None
    rv: Optional[List[APIClient]] = None

    # Get the resources
    with DatabaseSession(commit_on_end=False, expire_on_commit=False) \
            as session:
        # First, we get all API clients
        data_list = session.query(APIClient).filter(APIClient.user == req_user)

        logger.debug('get_api_clients: we have the global list of API ' +
                     'clients for this user')

        # Now, we can apply the correct filters
        try:
            if flt_id:
                flt_id = int(flt_id)
                data_list = data_list.filter(APIClient.id == flt_id)
                logger.debug('get_api_clients: list is filtered')
        except (ValueError, TypeError):
            logger.error(
                f'API client id should be of type {int}, not {type(flt_id)}.')
            raise FilterNotValidError(
                f'API client id should be of type {int}, not {type(flt_id)}.')

        # Get the data
        if flt_id:
            rv = data_list.first()
            if rv is None:
                raise NotFoundError(
                    f'API client with ID {flt_id} is not found.')
        else:
            rv = data_list.all()
            if len(rv) == 0:
                logger.debug('get_api_clients: no API clients to return')
                rv = None

    # Return the data
    logger.debug('get_api_clients: returning API clients')
    return rv


def update_api_client(
    req_user: User,
    api_client_id: int,
    **kwargs: dict
) -> Optional[APIClient]:
    """ Method to update a API client.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what the user is allowed to do.

        client_id : int
            The ID for the API client to change

        **kwargs : dict
            A dict containing the fields for the API client.

        Returns
        -------
        APIClient
            The updated API client object.

        None
            No API client updated.
    """

    # Get the resource object
    resource: Optional[Union[List[APIClient], APIClient]] = \
        get_api_clients(req_user, flt_id=api_client_id)

    logger.debug('update_api_client: we have the resource')

    # Check if we have all fields
    needed_fields = list()
    for field in needed_fields:
        if field not in kwargs.keys():
            raise TypeError(
                f'Missing required argument "{field}"')

    logger.debug('update_api_client: all needed fields are given')

    # Set the optional fields
    optional_fields = {
        'app_name': 'app_name',
        'app_publisher': 'app_publisher'
    }

    # Check if no other fields are given
    possible_fields = needed_fields + list(optional_fields.keys())
    for field in kwargs.keys():
        if field not in possible_fields:
            raise TypeError(
                f'Unexpected field "{field}"')

    # Update the resource
    for field in kwargs.keys():
        if field in optional_fields.keys():
            setattr(resource, optional_fields[field], kwargs[field])
        else:
            raise FilterNotValidError(
                f'Field {field} is not a valid field')

    # Save the fields
    try:
        with DatabaseSession(
            commit_on_end=True,
            expire_on_commit=True
        ) as session:
            logger.debug('update_api_client: merging resource into session')

            # Add the changed resource to the session
            session.merge(resource)

        # Done! Return the resource
        if isinstance(resource, APIClient):
            logger.debug('update_api_client: updating was a success!')
            return resource
    except sqlalchemy.exc.IntegrityError as e:
        # Add a custom text to the exception
        logger.error(
            f'update_api_client: sqlalchemy.exc.IntegrityError: {str(e)}')
        raise IntegrityError('API client already exists')

    return None


def delete_api_client(
    req_user: User,
    api_client_id: int
) -> bool:
    """ Method to delete a API client.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what the user is allowed to do.

        api_client_id : int
            The ID for the API client to delete.

        Returns
        -------
        bool
            True on success.
    """

    # Get the API client
    resource = get_api_clients(req_user=req_user, flt_id=api_client_id)

    logger.debug('delete_api_client: we have the resource')

    # Create a database session
    try:
        with DatabaseSession(
            commit_on_end=True,
            expire_on_commit=True
        ) as session:
            # Delete the resource
            logger.debug('delete_api_client: deleting the resource')
            session.delete(resource)
    except sqlalchemy.exc.IntegrityError as e:
        logger.error(
            f'delete_api_client: sqlalchemy.exc.IntegrityError: {str(e)}')
        raise IntegrityError(
            'API client couldn\'t be deleted because it still has resources ' +
            'connected to it')
    else:
        logger.debug('delete_api_client: return True because it was a success')
        return True
