"""
    Module that contains the methods to get tag details from the
    database.
"""
from typing import List, Optional
import sqlalchemy
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
