""" Module that contains the methods to get web ui setting details from the
    database. """

from typing import List, Optional, Union
import sqlalchemy
from sqlalchemy.orm.query import Query
from database import DatabaseSession
from my_database import validate_input
from my_database.field import Field
from my_database_model import WebUISetting, User
from my_database import logger
from my_database.exceptions import (FilterNotValidError, IntegrityError,
                                    NotFoundError)
from my_database.exceptions import (FilterNotValidError,
                                    IntegrityError, NotFoundError)


# Define the fields for validation
validation_fields = {
    'setting': Field(
        'setting',
        str,
        str_regex_validator=r'[A-Za-z][A-Za-z0-9\-_.]+'),
    'value': Field(
        'value',
        str)
}


def create_web_ui_setting(req_user: User, **kwargs: dict) -> Optional[WebUISetting]:
    """" Method to create a web ui setting

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what the user is allowed to do.

        **kwargs : dict
            A dict containing the fields for the setting.

        Returns
        -------
        WebUISetting
            The created WebUISetting object.

        None
            The WebUISetting was not created.
    """

    # Set the needed fields
    required_fields = {
        'setting': validation_fields['setting'],
        'value': validation_fields['value']
    }

    # Set the optional fields
    optional_fields = None

    # Validate the user input
    validate_input(
        input_values=kwargs,
        required_fields=required_fields,
        optional_fields=optional_fields)

    logger.debug('create_web_ui_setting: all arguments are validated')

    # Combine the arguments
    all_fields: dict = dict()
    if required_fields:
        all_fields.update(required_fields)
    if optional_fields:
        all_fields.update(optional_fields)

    try:
        with DatabaseSession(
            commit_on_end=True,
            expire_on_commit=True
        ) as session:
            # Create the resource
            new_resource = WebUISetting(user=req_user)

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

            logger.debug('create_web_ui_setting: adding setting')

            # Add the resource
            session.add(new_resource)

            # Return the created resource
            return new_resource
    except sqlalchemy.exc.IntegrityError as e:
        logger.error(f'create_web_ui_setting: IntegrityError: {str(e)}')
        # Add a custom text to the exception
        raise IntegrityError('Setting already exists')

    return None


def get_web_ui_settings(
    req_user: User,
    flt_id: Optional[int] = None,
    flt_setting: Optional[str] = None
) -> Optional[Union[List[WebUISetting], WebUISetting]]:
    """ Method that retrieves all, or a subset of, the web ui settings in the
        database.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what results the user gets.

        flt_id : Optional[int] [default=None]
            Filter on a specific web ui setting ID.

        flt_setting : Optional[str] [default=None]
            Filter on a specific web ui setting name.

        Returns
        -------
        List[WebUISetting]
            A list with the resulting setting.

        WebUISetting
            The found web ui setting (if filtered on a uniq value, like flt_id).

        None
            No settings are found.
    """

    # Empty data list
    data_list: Optional[Query] = None
    rv: Optional[List[WebUISetting]] = None

    # Get the resources
    with DatabaseSession(commit_on_end=False, expire_on_commit=False) \
            as session:
        # First, we get all web ui settings for this user
        data_list = session.query(WebUISetting).filter(
            WebUISetting.user == req_user)

        logger.debug(
            'get_web_ui_settings: we have the global list of web ui settings for this user')

        # Apply filter for ID
        try:
            if flt_id:
                flt_id = int(flt_id)
                data_list = data_list.filter(WebUISetting.id == flt_id)
                logger.debug('get_web_ui_settings: list is filtered on ID')
        except (ValueError, TypeError):
            logger.error(
                f'WebUISetting id should be of type {int}, not {type(flt_id)}.')
            raise FilterNotValidError(
                f'WebUISetting id should be of type {int}, not {type(flt_id)}.')

        # Apply filter for setting
        if flt_setting:
            flt_setting = flt_setting
            data_list = data_list.filter(
                WebUISetting.setting == flt_setting)
            logger.debug('get_web_ui_settings: list is filtered on setting')

        # Get the data
        if flt_id:
            rv = data_list.first()
            if rv is None:
                raise NotFoundError(
                    f'WebUISetting with ID {flt_id} is not found.')
        elif flt_setting:
            rv = data_list.first()
            if rv is None:
                raise NotFoundError(
                    f'WebUISetting with setting "{flt_setting}" is not found.')
        else:
            rv = data_list.all()
            if len(rv) == 0:
                logger.debug('get_web_ui_settings: no settings to return')
                rv = None

    # Return the data
    logger.debug('get_web_ui_settings: returning settings')
    return rv


def update_web_ui_setting(
    req_user: User,
    setting_id: int,
    **kwargs: dict
) -> Optional[WebUISetting]:
    """ Method to update a setting.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what the user is allowed to do.

        setting_id : int
            The ID for the web ui setting to change

        **kwargs : dict
            A dict containing the fields for the web ui setting.

        Returns
        -------
        WebUISetting
            The updated WebUISetting object.

        None
            No WebUISetting updated.
    """

    # Get the resource object
    resource: Optional[Union[List[WebUISetting], WebUISetting]
                       ] = get_web_ui_settings(req_user, flt_id=setting_id)

    logger.debug('update_web_ui_setting: we have the resource')

    # Set the needed fields
    required_fields = {
        'value': validation_fields['value'],
    }

    # Set the optional fields
    optional_fields = {
        'setting': validation_fields['setting'],
    }

    # Validate the user input
    validate_input(
        input_values=kwargs,
        required_fields=required_fields,
        optional_fields=optional_fields)

    logger.debug('update_web_ui_setting: all arguments are validated')

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
            logger.debug(
                'update_web_ui_setting: merging resource into session')

            # Add the changed resource to the session
            session.merge(resource)

        # Done! Return the resource
        if isinstance(resource, WebUISetting):
            logger.debug('update_web_ui_setting: updating was a success!')
            return resource
    except sqlalchemy.exc.IntegrityError as e:
        # Add a custom text to the exception
        logger.error(
            f'update_web_ui_setting: sqlalchemy.exc.IntegrityError: {str(e)}')
        raise IntegrityError('WebUISetting already exists')

    return None


def delete_web_ui_setting(
    req_user: User,
    setting_id: int
) -> bool:
    """ Method to delete a web ui setting.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what the user is allowed to do.

        setting_id : int
            The ID for the setting to delete.

        Returns
        -------
        bool
            True on success.
    """

    # Get the WebUISetting
    resource = get_web_ui_settings(req_user=req_user, flt_id=setting_id)

    logger.debug('delete_web_ui_setting: we have the resource')

    # Create a database session
    try:
        with DatabaseSession(
            commit_on_end=True,
            expire_on_commit=True
        ) as session:
            # Delete the resource
            logger.debug('delete_web_ui_setting: deleting the resource')
            session.delete(resource)
    except sqlalchemy.exc.IntegrityError as e:
        logger.error(
            f'delete_web_ui_setting: sqlalchemy.exc.IntegrityError: {str(e)}')
        raise IntegrityError(
            'WebUISetting couldn\'t be deleted because it still has resources ' +
            'connected to it')
    else:
        logger.debug(
            'delete_web_ui_setting: return True because it was a success')
        return True
