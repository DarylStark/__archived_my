"""
    Module that contains the methods to get tag details from the
    database.
"""
from typing import List, Optional
from database import DatabaseSession
from my_database.generic import delete_object
from my_database_model import User, Tag
from sqlalchemy.orm.query import Query
from my_database import logger
from my_database.exceptions import FilterNotValidError, IntegrityError, NotFoundError


def get_tags(
    req_user: Optional[User],
    flt_id: Optional[int] = None
) -> Optional[List[Tag]]:
    """ Method that retrieves all, or a subset of, the tags in the
        database.

        Parameters
        ----------
        req_user : User
            The user who is requesting this. Should be used to verify
            what results the user gets. If this is set to 'None',
            we bypass this check.

        flt_id : Optional[int]
            Filter on a specific tag ID.

        Returns
        -------
        List[Tag]
            A list with the resulting tags.

        None
            No tags are found.
    """

    # Empty data list
    data_list: Optional[Query] = None
    rv: Optional[List[Tag]] = None

    # Get the token
    with DatabaseSession(commit_on_end=False, expire_on_commit=False) \
            as session:
        # First, we get all tags
        data_list = session.query(Tag)

        # If a user is specified, we use that user to filter the tags
        if req_user:
            data_list = data_list.filter(Tag.user_id == req_user.id)

        # Now, we can apply the correct filters
        try:
            if flt_id:
                flt_id = int(flt_id)
                data_list = data_list.filter(Tag.id == flt_id)
        except (ValueError, TypeError):
            logger.error(
                f'Tag id should be of type {int}, not {type(flt_id)}.')
            raise FilterNotValidError(
                f'Tag id should be of type {int}, not {type(flt_id)}.')

        # Get the data
        if data_list is not None:
            rv = data_list.all()

    # Return the data
    return rv


def delete_tag(
    req_user: Optional[User],
    tag_id: int
) -> bool:
    """ Method to delete a tag.

        Parameters
        ----------
        req_user : Optional[User]
            The user who is requesting this. Should be used to verify
            what the user is allowed to do. If this is set to 'None',
            we bypass this check.

        tag_id : int
            The ID for the tag to delete.

        Returns
        -------
        bool
            True on success.
    """

    # Get the resource object
    resource: Optional[List[Tag]] = get_tags(req_user, flt_id=tag_id)

    # Check if we got a resource. If we didn't, we rise an error
    # indicating that the resource wasn't found. This can be either
    # because it didn't exist, or because the user has no permissions
    # to it.
    if resource is None or len(resource) == 0:
        raise NotFoundError(f'Tag with ID {tag_id} is not found.')

    # Appearently we have resources. Because the result is a list, we
    # we can assume the first one in the list is the one we are
    # interested in.
    resource = resource[0]

    # Delete the resource
    try:
        # Delete the resource itself
        delete_object(resource)
    except IntegrityError:
        # Add a custom text to the exception
        raise IntegrityError(
            'Tag couldn\'t be deleted because it still has resources ' +
            'connected to it')
    else:
        return True
