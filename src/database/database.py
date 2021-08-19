"""
    Module that contains the static 'Database' class. This class can
    and should be used to communicate with the database.
"""
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from database.exceptions import DatabaseConnectionError


class Database:
    """ Main class for the Database object. Will be an static class
        that cannot be initiated. """

    # Static variables are used by the static class
    _engine = None
    base_class = declarative_base()
    session = sessionmaker()

    # Methods to make sure this class is used as it is suppoes to be
    def __new__(cls) -> None:
        """ When someone tries to create a instance of the Database
            class, we give an TypeError. This is done because this
            class should be a static class.

            Parameters
            ----------
            None

            Returns
            -------
            None
        """

        raise TypeError(
            f'It is impossible to create a instance of class "{cls.__name__}"')

    @classmethod
    def connect(cls,
                connection: str,
                echo: bool = False,
                pool_pre_ping: bool = True,
                pool_recycle: int = 10,
                pool_size: int = 5,
                pool_overflow: int = 10,
                create_tables: bool = False,
                drop_tables_first: bool = False) -> None:
        """ Method to create a SQLAlchemy engine. Uses the database and
            credentials given by the user. Since this is a static
            class, we set it in the class parameter. This way, the
            complete application uses the same database engine. After
            creating the engine, it calls the command to create the
            tables in the database.

            Parameters
            ----------
            conncection : str
                The connection string that can be used by SQLalchemy.

            echo : bool
                Can be used for debugging; writes the queries for
                SQLAlchemy to the stdout buffer.

            pool_pre_ping : bool
                By default True. Determines if SQLAlchemy should
                do a pre-check before using a connection that is
                already in the pool. By doing this, we can prevent
                it from using dead connections.

            pool_recycle : int
                After how many seconds SQLAlchemy considers a
                MySQL connection to be stale and therefore removed
                from the database.

            pool_size : int
                The size the pool can get.

            pool_overflow : int
                How many connections SQLAlchemy can go over the
                pool_size.

            create_tables : bool
                Specifies if the method should create tables.

            drop_tables_first : bool
                Specifies if the method should drop tables.


            Returns
            -------
            None
        """

        try:
            # Create the engine
            cls._engine = create_engine(
                connection,
                echo=echo,
                pool_pre_ping=pool_pre_ping,
                pool_recycle=pool_recycle,
                pool_size=pool_size,
                max_overflow=pool_overflow
            )

            # If the user request the tables to be dropped first, we do
            # that now
            if drop_tables_first:
                cls.base_class.metadata.drop_all(cls._engine)

            # Create the configured tables, if the user requested to do
            # this
            if create_tables:
                cls.base_class.metadata.create_all(cls._engine)

            # Bind the engine to the sessionmaker of the class
            cls.session.configure(bind=cls._engine)
        except sqlalchemy.exc.OperationalError:
            raise DatabaseConnectionError('Couldn\'t connect to database')

    @classmethod
    def get_pool_statistics(cls) -> dict:
        """ Method that returns pool statistics, like the pool size,
            the amount of checked-in connections, the overflow and the
            checked out connections.

            Parameters
            ----------
            None

            Returns
            -------
            dict
                The requested statistics
        """

        return {
            'pool_size': cls._engine.pool.size(),
            'checked_in': cls._engine.pool.checkedin(),
            'overflow': cls._engine.pool.overflow(),
            'checked_out': cls._engine.pool.checkedout()
        }
