""" Module that contains the methods to get date tag details from the
    database. """

from typing import List, Optional, Union
import sqlalchemy
from sqlalchemy.orm.query import Query
from database import DatabaseSession
from my_database import validate_input
from my_database.field import Field
from my_database_model import Tag, User, DateTag
from my_database.tags import get_tags
from my_database import logger
from my_database.exceptions import (FilterNotValidError, IntegrityError,
                                    NotFoundError)
from my_database.exceptions import (FilterNotValidError,
                                    IntegrityError, NotFoundError)

# Define the fields for validation
validation_fields = {
    'date': Field(
        'date',
        str,
        str_regex_validator=r'[0-9]{4}-[0-9]{2}-[0-9]{2}+'),
    'tag_id': Field(
        'tag_id',
        int)
}


def create_date_tag(req_user: User, **kwargs: dict) -> Optional[Tag]:
    """" Method to create a date tag

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what the user is allowed to do.

        **kwargs : dict
            A dict containing the fields for the date tag.

        Returns
        -------
        DateTag
            The created date tag object.

        None
            The date tag was not created.
    """

    # Set the needed fields
    required_fields = {
        'date': validation_fields['date'],
        'tag_id': validation_fields['tag_id']
    }

    # Set the optional fields
    optional_fields = None

    # Validate the user input
    validate_input(
        input_values=kwargs,
        required_fields=required_fields,
        optional_fields=optional_fields)

    logger.debug('create_date_tag: all arguments are validated')

    # Combine the arguments
    all_fields: dict = dict()
    if required_fields:
        all_fields.update(required_fields)
    if optional_fields:
        all_fields.update(optional_fields)

    # Search for the tag to see if it is the same user as the user who is
    # requesting this
    tag = get_tags(req_user, flt_id=all_fields['tag_id'])
    if tag is None:
        # TODO: RAISE ERROR
        return None

    try:
        with DatabaseSession(
            commit_on_end=True,
            expire_on_commit=False
        ) as session:
            # Create the resource
            new_resource = DateTag()

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

            logger.debug('create_date_tag: adding tag')

            # Add the resource
            session.add(new_resource)

            # Return the created resource
            return new_resource
    except sqlalchemy.exc.IntegrityError as e:
        logger.error(f'create_date_tag: IntegrityError: {str(e)}')
        # Add a custom text to the exception
        raise IntegrityError('DateTag already exists')

    return None


def get_date_tags(
    req_user: User,
    flt_id: Optional[int] = None,
    flt_date: Optional[str] = None
) -> Optional[Union[List[Tag], Tag]]:
    """ Method that retrieves all, or a subset of, the date tags in the
        database.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what results the user gets.

        flt_id : Optional[int] [default=None]
            Filter on a specific date tag ID.

        flt_date : Optional[str] [default=None]
            Filter on a specific date.

        Returns
        -------
        List[DateTag]
            A list with the resulting date tags.

        Tag
            The found date tag (if filtered on a uniq value, like flt_id).

        None
            No date tags are found.
    """

    # Empty data list
    data_list: Optional[Query] = None
    rv: Optional[List[Tag]] = None

    # Get the resources
    with DatabaseSession(commit_on_end=False, expire_on_commit=False) \
            as session:
        # First, we get all tags for this user
        data_list = session.query(DateTag).filter(DateTag.Tag.user == req_user)

        logger.debug(
            'get_date_tags: we have the global list of date tags for this user')

        # Apply filter for ID
        try:
            if flt_id:
                flt_id = int(flt_id)
                data_list = data_list.filter(DateTag.id == flt_id)
                logger.debug('get_date_tags: list is filtered on ID')
        except (ValueError, TypeError):
            logger.error(
                f'Tag id should be of type {int}, not {type(flt_id)}.')
            raise FilterNotValidError(
                f'Tag id should be of type {int}, not {type(flt_id)}.')

        # Apply filter for title
        if flt_date:
            data_list = data_list.filter(TDateTag.date == flt_date)
            logger.debug('get_date_tags: list is filtered on date')

        # Get the data
        if flt_id:
            rv = data_list.first()
            if rv is None:
                raise NotFoundError(
                    f'DateTag with ID {flt_id} is not found.')
        elif flt_date:
            rv = data_list.first()
            if rv is None:
                raise NotFoundError(
                    f'DateTag with date "{flt_date}" is not found.')
        else:
            rv = data_list.all()
            if len(rv) == 0:
                logger.debug('get_date_tags: no datetags to return')
                rv = None

    # Return the data
    logger.debug('get_date_tags: returning users')
    return rv


def delete_date_tags(
    req_user: User,
    date_tag_ids: Union[List[int], int]
) -> bool:
    """ Method to delete a date tag.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what the user is allowed to do.

        date_tag_id : Union[List[int], int]
            A list of date tags to delete or a date tag ID

        Returns
        -------
        bool
            True on success.
    """

    # Get the tag
    resources = None
    if type(date_tag_ids) is list:
        resources = [
            get_date_tags(req_user=req_user, flt_id=r)
            for r in date_tag_ids
        ]
    else:
        resources = [get_date_tags(req_user=req_user, flt_id=date_tag_ids)]

    logger.debug('delete_date_tags: we have the resources')

    # Create a database session
    try:
        with DatabaseSession(
            commit_on_end=True,
            expire_on_commit=True
        ) as session:
            # Delete the resource
            logger.debug('delete_date_tags: deleting the resources')
            for resource in resources:
                session.delete(resource)
    except sqlalchemy.exc.IntegrityError as e:
        logger.error(
            f'delete_date_tags: sqlalchemy.exc.IntegrityError: {str(e)}')
        raise IntegrityError(
            'DateTag couldn\'t be deleted because it still has resources ' +
            'connected to it')
    else:
        logger.debug('delete_date_tags: return True because it was a success')
        return True
