"""
    Module that contains the generic database methods
"""
from typing import List, Optional
from database import DatabaseSession, Database
import sqlalchemy.exc
from my_database.exceptions import IntegrityError


def add_object(obj: Database.base_class) -> bool:
    """ Method to add objects to the database.

        Parameters
        ----------
        obj : Database.base_class
            The object to add.

        Returns
        -------
        Boolean
            True when the operation was a success, False when the
            operation failed.
    """

    # Create a database session and add the model
    try:
        with DatabaseSession(commit_on_end=True, expire_on_commit=False) \
                as session:
            session.add(obj)
    except sqlalchemy.exc.IntegrityError:
        raise IntegrityError
    else:
        return True


def update_object(obj: Database.base_class) -> bool:
    """ Method to update objects in the database.

        Parameters
        ----------
        obj : Database.base_class
            The object to update.

        Returns
        -------
        Boolean
            True when the operation was a success, False when the
            operation failed.
    """
    # Create a database session and update the model
    try:
        with DatabaseSession(commit_on_end=True, expire_on_commit=False) \
                as session:
            session.merge(obj)
    except sqlalchemy.exc.IntegrityError:
        raise IntegrityError
    else:
        return True


def delete_object(obj: Database.base_class) -> bool:
    """ Method to delete objects from the database.

        Parameters
        ----------
        obj : Database.base_class
            The object to delete.

        Returns
        -------
        Boolean
            True when the operation was a success, False when the
            operation failed.
    """
    # Create a database session and delete the model
    try:
        with DatabaseSession(commit_on_end=True, expire_on_commit=False) \
                as session:
            session.delete(obj)
    except sqlalchemy.exc.IntegrityError:
        raise IntegrityError
    else:
        return True
