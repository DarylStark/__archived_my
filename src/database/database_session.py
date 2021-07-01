"""
    Module that contains the DatabaseSession class. Can be used as
    context manager to communicate with the database in a safe manner.
"""
from types import TracebackType
from typing import Optional, Type

from sqlalchemy.orm.session import Session

from database import Database


class DatabaseSession:
    """ Class for database session. Can and should be used as context
        manager. """

    def __init__(self,
                 commit_on_end: bool = False,
                 expire_on_commit: bool = True) -> None:
        """ The initiator creates an empty session to use with this
            object. When 'expire_on_commit' is set, all objects that
            were added during this session are expired after the
            session is commited.

            Parameters
            ----------
            commit_on_end : bool, default=False
                Tells the object to commit when the context manager is
                done.

            expire_on_commit : bool, default=True
                Tells the object to either expire or not expire created
                objects after the context manager is done.

            Returns
            -------
            None
        """

        self.session: Session = Database.session(
            expire_on_commit=expire_on_commit)
        self.commit_on_end = commit_on_end

    def close(self) -> None:
        """ Closes the session.

            Parameters
            ----------
            None

            Returns
            -------
            None
        """
        self.session.close()

    def commit(self) -> None:
        """ Commits the session.

            Parameters
            ----------
            None

            Returns
            -------
            None
        """
        self.session.commit()

    def rollback(self) -> None:
        """ Rolls back the session.

            Parameters
            ----------
            None

            Returns
            -------
            None
        """
        self.session.rollback()

    def __enter__(self) -> Session:
        """ Context manager for the session. Makes sure you can use the
            session as Context Manager and prevents errors.

            Parameters
            ----------
            None

            Returns
            -------
            session
                The database session
        """
        return self.session

    def __exit__(self,
                 exception_type: Optional[Type[BaseException]],
                 exception_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> bool:
        """ The end of the context manager. Commits the session (if the
            user requested this) and closes the session.

            Parameters
            ----------
            exception_type : Optional[Type[BaseException]]
                The exception that happend during execution.

            exception_value : Optional[BaseException]
                The value of the exception.

            traceback : Optional[TracebackType]
                The traceback for the exception.

            Returns
            -------
            bool
            True is everything went fine, False if there was an
            exception.
        """

        # Commit, if needed
        if self.commit_on_end:
            self.commit()

        # Close the session
        self.close()

        # If 'type' is None, there was no error so we can return True.
        # Otherwise, False is returned and the exception is passed
        # through
        return exception_type is None
