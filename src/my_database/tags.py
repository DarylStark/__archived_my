""" Module that contains the methods to get tag details from the
    database. """

from typing import List, Optional, Union
import sqlalchemy
from sqlalchemy.orm.query import Query
from database import DatabaseSession
from my_database import validate_input
from my_database.field import Field
from my_database_model import Tag, User
from my_database import logger
from my_database.exceptions import (FilterNotValidError, IntegrityError,
                                    NotFoundError)
from my_database.exceptions import (FilterNotValidError,
                                    IntegrityError, NotFoundError)

# Define the fields for validation
validation_fields = {
    'title': Field(
        'title',
        str,
        str_regex_validator=r'[A-Za-z][A-Za-z0-9\-. ]+'),
    'color': Field(
        'color',
        str,
        str_regex_validator=r'([A-Fa-f0-9]{3}|[A-Fa-f0-9]{6})'),
    'tag_ids': Field(
        'tag_ids',
        list),
    'tag_id': Field(
        'tag_id',
        int)
}


def create_tag(req_user: User, **kwargs: dict) -> Optional[Tag]:
    """" Method to create a tag

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what the user is allowed to do.

        **kwargs : dict
            A dict containing the fields for the tag.

        Returns
        -------
        Tag
            The created tag object.

        None
            The tag was not created.
    """

    # Set the needed fields
    required_fields = {
        'title': validation_fields['title']
    }

    # Set the optional fields
    optional_fields = {
        'color': validation_fields['color']
    }

    # Validate the user input
    validate_input(
        input_values=kwargs,
        required_fields=required_fields,
        optional_fields=optional_fields)

    logger.debug('create_tag: all arguments are validated')

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
            new_resource = Tag(user=req_user)

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

            logger.debug('create_tag: adding tag')

            # Add the resource
            session.add(new_resource)

            # Return the created resource
            return new_resource
    except sqlalchemy.exc.IntegrityError as e:
        logger.error(f'create_tag: IntegrityError: {str(e)}')
        # Add a custom text to the exception
        raise IntegrityError('Tag already exists')

    return None


def get_tags(
    req_user: User,
    flt_id: Optional[int] = None,
    flt_title: Optional[str] = None
) -> Optional[Union[List[Tag], Tag]]:
    """ Method that retrieves all, or a subset of, the tags in the
        database.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what results the user gets.

        flt_id : Optional[int] [default=None]
            Filter on a specific tag ID.

        flt_title : Optional[str] [default=None]
            Filter on a specific tag title.

        Returns
        -------
        List[Tag]
            A list with the resulting tags.

        Tag
            The found tag (if filtered on a uniq value, like flt_id).

        None
            No tags are found.
    """

    # Empty data list
    data_list: Optional[Query] = None
    rv: Optional[List[Tag]] = None

    # Get the resources
    with DatabaseSession(commit_on_end=False, expire_on_commit=False) \
            as session:
        # First, we get all tags for this user
        data_list = session.query(Tag).filter(Tag.user == req_user)

        logger.debug('get_tags: we have the global list of tags for this user')

        # Apply filter for ID
        try:
            if flt_id:
                flt_id = int(flt_id)
                data_list = data_list.filter(Tag.id == flt_id)
                logger.debug('get_tags: list is filtered on ID')
        except (ValueError, TypeError):
            logger.error(
                f'Tag id should be of type {int}, not {type(flt_id)}.')
            raise FilterNotValidError(
                f'Tag id should be of type {int}, not {type(flt_id)}.')

        # Apply filter for title
        if flt_title:
            flt_title = flt_title
            data_list = data_list.filter(Tag.title == flt_title)
            logger.debug('get_tags: list is filtered on title')

        # Get the data
        if flt_id:
            rv = data_list.first()
            if rv is None:
                raise NotFoundError(
                    f'Tag with ID {flt_id} is not found.')
        elif flt_title:
            rv = data_list.first()
            if rv is None:
                raise NotFoundError(
                    f'Tag with title "{flt_title}" is not found.')
        else:
            rv = data_list.all()
            if len(rv) == 0:
                logger.debug('get_tags: no users to return')
                rv = None

    # Return the data
    logger.debug('get_tags: returning users')
    return rv


def update_tag(
    req_user: User,
    tag_id: int,
    **kwargs: dict
) -> Optional[Tag]:
    """ Method to update a tag.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what the user is allowed to do.

        tag_id : int
            The ID for the tag to change

        **kwargs : dict
            A dict containing the fields for the tag.

        Returns
        -------
        Tag
            The updated tag object.

        None
            No tag updated.
    """

    # Get the resource object
    resource: Optional[Union[List[Tag], Tag]] = \
        get_tags(req_user, flt_id=tag_id)

    logger.debug('update_tag: we have the resource')

    # Set the needed fields
    required_fields = None

    # Set the optional fields
    optional_fields = {
        'title': validation_fields['title'],
        'color': validation_fields['color']
    }

    # Validate the user input
    validate_input(
        input_values=kwargs,
        required_fields=required_fields,
        optional_fields=optional_fields)

    logger.debug('update_tag: all arguments are validated')

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
            logger.debug('update_tag: merging resource into session')

            # Add the changed resource to the session
            session.merge(resource)

        # Done! Return the resource
        if isinstance(resource, Tag):
            logger.debug('update_tag: updating was a success!')
            return resource
    except sqlalchemy.exc.IntegrityError as e:
        # Add a custom text to the exception
        logger.error(
            f'update_tag: sqlalchemy.exc.IntegrityError: {str(e)}')
        raise IntegrityError('Tag already exists')

    return None


def delete_tags(
    req_user: User,
    tag_id: Union[List[int], int]
) -> bool:
    """ Method to delete a tag.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what the user is allowed to do.

        tag_id : Union[List[int], int]
            A list of tags to delete or a tag ID

        Returns
        -------
        bool
            True on success.
    """

    # Get the tag
    resources = None
    if type(tag_id) is list:
        resources = [
            get_tags(req_user=req_user, flt_id=r)
            for r in tag_id
        ]
    else:
        resources = [get_tags(req_user=req_user, flt_id=tag_id)]

    logger.debug('delete_tag: we have the resources')

    # Create a database session
    try:
        with DatabaseSession(
            commit_on_end=True,
            expire_on_commit=True
        ) as session:
            # Delete the resource
            logger.debug('delete_tag: deleting the resources')
            for resource in resources:
                session.delete(resource)
    except sqlalchemy.exc.IntegrityError as e:
        logger.error(
            f'delete_tag: sqlalchemy.exc.IntegrityError: {str(e)}')
        raise IntegrityError(
            'Tag couldn\'t be deleted because it still has resources ' +
            'connected to it')
    else:
        logger.debug('delete_tag: return True because it was a success')
        return True
