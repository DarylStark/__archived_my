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
                                    IntegrityError, PermissionDeniedError,
                                    NotFoundError)
from rest_api_generator.exceptions import ServerError


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
    except Exception as e:
        logger.error(f'create_tag: Exception: {str(e)}')
        raise ServerError(e)

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
