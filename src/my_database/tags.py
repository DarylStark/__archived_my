"""
    Module that contains the methods to get tag details from the
    database.
"""
from typing import List, Optional, Union
import sqlalchemy
from sqlalchemy.orm.query import Query
from database import DatabaseSession
from my_database_model import Tag, User
from my_database import logger
from my_database.exceptions import (FilterNotValidError, IntegrityError,
                                    NotFoundError)
from my_database.exceptions import (FilterNotValidError,
                                    IntegrityError, NotFoundError)


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

    """

    # Check if we have all fields
    needed_fields = [
        'title'
    ]
    for field in needed_fields:
        if field not in kwargs.keys():
            raise TypeError(
                f'Missing required argument "{field}"')

    logger.debug('create_tag: all needed fields are given')

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
            new_resource = Tag(
                user=req_user,
                title=kwargs['title']
            )

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
    flt_id: Optional[int] = None
) -> Optional[Union[List[Tag], Tag]]:
    """ Method that retrieves all, or a subset of, the tags in the
        database.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what results the user gets.

        flt_id : Optional[int]
            Filter on a specific tag ID.

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
    rv: Optional[List[Ta]] = None

    # Get the resources
    with DatabaseSession(commit_on_end=False, expire_on_commit=False) \
            as session:
        # First, we get all tags for this user
        data_list = session.query(Tag).filter(Tag.user == req_user)

        logger.debug('get_tags: we have the global list of tags for this user')

        # Now, we can apply the correct filters
        try:
            if flt_id:
                flt_id = int(flt_id)
                data_list = data_list.filter(Tag.id == flt_id)
                logger.debug('get_tags: list is filtered')
        except (ValueError, TypeError):
            logger.error(
                f'Tag id should be of type {int}, not {type(flt_id)}.')
            raise FilterNotValidError(
                f'Tag id should be of type {int}, not {type(flt_id)}.')

        # Get the data
        if flt_id:
            rv = data_list.first()
            if rv is None:
                raise NotFoundError(
                    f'Tag with ID {flt_id} is not found.')
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

    # Check if we have all fields
    needed_fields = list()
    for field in needed_fields:
        if field not in kwargs.keys():
            raise TypeError(
                f'Missing required argument "{field}"')

    logger.debug('update_tag: all needed fields are given')

    # Set the optional fields
    optional_fields = {
        'title': 'title'
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


def delete_tag(
    req_user: User,
    tag_id: int
) -> bool:
    """ Method to delete a tag.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what the user is allowed to do.

        tag_id : int
            The ID for the tag to delete.

        Returns
        -------
        bool
            True on success.
    """

    # Get the tag
    resource = get_tags(req_user=req_user, flt_id=tag_id)

    logger.debug('delete_tag: we have the resource')

    # Create a database session
    try:
        with DatabaseSession(
            commit_on_end=True,
            expire_on_commit=True
        ) as session:
            # Delete the resource
            logger.debug('delete_tag: deleting the resource')
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
