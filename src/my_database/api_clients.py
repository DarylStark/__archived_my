""" Module that contains the methods to get and set api client details
    from the database. """

from typing import List, Optional, Union
from my_database.field import Field
import sqlalchemy
from database import DatabaseSession
from my_database import validate_input
from my_database_model import APIClient, User
from sqlalchemy.orm.query import Query
from my_database import logger
from datetime import datetime
from my_database.exceptions import (FilterNotValidError,
                                    IntegrityError, NotFoundError)

# Define the fields for validation
validation_fields = {
    'app_name': Field(
        'app_name',
        str,
        str_regex_validator=r'[A-Za-z][A-Za-z0-9\-_. ]+'),
    'app_publisher': Field(
        'app_publisher',
        str,
        str_regex_validator=r'[A-Za-z][A-Za-z0-9\-_. ]+'),
    'redirect_url': Field('redirect_url', str),
    'enabled': Field('enabled', bool),
    'expires': Field('expires', datetime),
    'api_client_ids': Field(
        'tag_ids',
        list),
    'client_id': Field('client_id', int),
}


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

        None:
            The API client was not created.
    """

    # Set the needed fields
    required_fields = {
        'app_name': validation_fields['app_name'],
        'app_publisher': validation_fields['app_publisher']
    }

    # Set the optional fields
    optional_fields = {
        'enabled': validation_fields['enabled'],
        'expires': validation_fields['expires'],
        'redirect_url': validation_fields['redirect_url']
    }

    # Validate the user input
    validate_input(
        input_values=kwargs,
        required_fields=required_fields,
        optional_fields=optional_fields)

    logger.debug('create_api_client: all arguments are validated')

    # Combine the arguments
    all_fields: dict = dict()
    if required_fields:
        all_fields.update(required_fields)
    if optional_fields:
        all_fields.update(optional_fields)

    try:
        with DatabaseSession(
            commit_on_end=True,
            expire_on_commit=False
        ) as session:
            # Create the resource
            new_resource = APIClient(user=req_user)

            # Set the fields
            for field in kwargs.keys():
                if field in all_fields.keys():
                    if hasattr(new_resource, all_fields[field].object_field):
                        setattr(
                            new_resource,
                            all_fields[field].object_field,
                            kwargs[field])
                    else:
                        raise AttributeError(
                            f"'{type(new_resource)}' has no attribute " +
                            f"'{all_fields[field].object_field}'"
                        )
                else:
                    raise FilterNotValidError(
                        f'Field {field} is not a valid field')

            # Set token
            new_resource.generate_random_token()

            logger.debug('create_api_client: adding API client')

            # Add the resource
            session.add(new_resource)

            # Return the created resource
            return new_resource
    except sqlalchemy.exc.IntegrityError as e:
        logger.error(f'create_api_client: IntegrityError: {str(e)}')
        # Add a custom text to the exception
        raise IntegrityError('API client already exists')

    return None


def get_api_clients(
    req_user: User,
    flt_id: Optional[int] = None,
    flt_token: Optional[str] = None,
    flt_enabled: Optional[bool] = None,
) -> Optional[Union[List[APIClient], APIClient]]:
    """ Method that retrieves all, or a subset of, the API clients in
        the database.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what results the user gets.

        flt_id : Optional[int] [default=None]
            Filter on a specific client ID.

        flt_id : Optional[int] [default=None]
            Filter on a specific token ID.

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

        try:
            if flt_token:
                flt_token = str(flt_token)
                data_list = data_list.filter(APIClient.token == flt_token)
                logger.debug('get_api_clients: list is filtered on token')
        except (ValueError, TypeError):
            logger.error(
                f'API token should be of type {str}, not {type(flt_id)}.')
            raise FilterNotValidError(
                f'API token should be of type {str}, not {type(flt_id)}.')

        try:
            if flt_enabled is not None:
                flt_enabled = bool(flt_enabled)
                data_list = data_list.filter(APIClient.enabled == flt_enabled)
                logger.debug(
                    'get_api_clients: list is filtered on enable-status')
        except (ValueError, TypeError):
            logger.error(
                f'API enabled should be of type {bool}, not {type(flt_id)}.')
            raise FilterNotValidError(
                f'API enabled should be of type {bool}, not {type(flt_id)}.')

        # Get the data
        if flt_id or flt_token:
            rv = data_list.first()
            if rv is None:
                raise NotFoundError(
                    f'API client is not found.')
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

    # Set the needed fields
    required_fields = None

    # Set the optional fields
    optional_fields = {
        'app_name': validation_fields['app_name'],
        'app_publisher': validation_fields['app_publisher'],
        'redirect_url': validation_fields['redirect_url'],
        'enabled': validation_fields['enabled'],
        'expires': validation_fields['expires']
    }

    # Validate the user input
    validate_input(
        input_values=kwargs,
        required_fields=required_fields,
        optional_fields=optional_fields)

    logger.debug('update_api_client: all arguments are validated')

    # Combine the arguments
    all_fields: dict = dict()
    if required_fields:
        all_fields.update(required_fields)
    if optional_fields:
        all_fields.update(optional_fields)

    # Update the resource
    for field in kwargs.keys():
        if field in all_fields.keys():
            if hasattr(resource, all_fields[field].object_field):
                setattr(
                    resource,
                    all_fields[field].object_field,
                    kwargs[field])
            else:
                raise AttributeError(
                    f"'{type(resource)}' has no attribute " +
                    f"'{all_fields[field].object_field}'"
                )
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


def delete_api_clients(
    req_user: User,
    api_client_id: Union[List[int], int]
) -> bool:
    """ Method to delete a API client.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what the user is allowed to do.

        api_client_id : Union[List[int], int]
            A list API clients to delete or a API client ID

        Returns
        -------
        bool
            True on success.
    """

    # Get the API client
    resources = None
    if type(api_client_id) is list:
        resources = [
            get_api_clients(req_user=req_user, flt_id=r)
            for r in api_client_id
        ]
    else:
        resources = [get_api_clients(req_user=req_user, flt_id=api_client_id)]

    logger.debug('delete_api_client: we have the resource')

    # Create a database session
    try:
        with DatabaseSession(
            commit_on_end=True,
            expire_on_commit=True
        ) as session:
            # Delete the resource
            logger.debug('delete_api_client: deleting the resource')
            for resource in resources:
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
