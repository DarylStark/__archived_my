"""
    Script to create the missing tables from the database
"""
import argparse
import logging
import os
import sys
import pymysql
import sqlalchemy
from rich.logging import RichHandler
from set_environment import set_environment

# Add include path. We need to do this because we are not in the
# original path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(
        __file__), os.path.pardir)) + '/src'
)
from database import Database, DatabaseSession
from database.exceptions import DatabaseConnectionError
from my_database_model import *

if __name__ == '__main__':
    # Parse the arguments for the script
    parser = argparse.ArgumentParser(description='Create the database')
    parser.add_argument('environment_file',
                        metavar='environment_file',
                        type=str,
                        help='The environment file with the settings')
    parser.add_argument('--create-data',
                        action='store_true',
                        help='Wheter or not testdata should be created')
    parser.add_argument('--drop-tables',
                        action='store_true',
                        help='Wheter or not the tables should be dropped')

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(level=logging.DEBUG, format="%(message)s",
                        datefmt="[%X]", handlers=[RichHandler()])
    logger = logging.getLogger(name='database-create')

    # Set the environment
    set_environment(args.environment_file, logger)

    # Get the database credentials
    username = os.environ["DB_USERNAME"]
    password = os.environ["DB_PASSWORD"]
    server = os.environ["DB_SERVER"]
    database = os.environ["DB_DATABASE"]

    # Connect to the database and create the needed tables
    logger.info(f'Connecting to database "{database}" on server "{server}"')
    connection_string = \
        f'mysql+pymysql://{username}:{password}@{server}/{database}'

    try:
        Database.connect(
            connection=connection_string,
            create_tables=True,
            drop_tables_first=args.drop_tables
        )
    except DatabaseConnectionError:
        logger.critical('Couldn\'t connect to the database!')
        sys.exit(1)

    # Add test data
    if args.create_data:
        # Define the objects to create. We define these objects in a
        # list and set the password as plaintext. In the loop where we
        # add the objects, we set the password using the correct
        # method.

        # The API token will be connected to a user later on. We create
        # the scopes
        scopes = [
            'api.ping', 'api.auth', 'users.create', 'users.retrieve', 'users.update',
            'users.delete', 'tags.create', 'tags.retrieve', 'tags.update',
            'tags.delete', 'date_tags.create', 'date_tags.retrieve', 'date_tags.delete'
        ]
        api_token_objects = [
            APIToken(
                expires=None,
                enabled=True,
                token='poiuytrewq',
                token_scopes=[
                    APITokenScope(
                        scope=APIScope(
                            module=x.split('.')[0],
                            subject=x.split('.')[1]
                        )
                    )
                    for x in scopes
                ]
            )
        ]

        # The user objects to create. We connect the needed objects for
        # these user immidiatly.
        user_objects = [
            User(
                fullname='Root user',
                username='root',
                email='root@dstark.nl',
                role=UserRole.root,
                password='mJZxFt0e65!w#WIkL92u9pc%Rt5VEYJ5yf^^ejeRZ2',
                tags=[
                    Tag(title='Root - Testtag1'),
                    Tag(title='Root - Testtag2')
                ]
            ),
            User(
                fullname='Daryl Stark',
                username='daryl.stark',
                email='daryl@dstark.nl',
                role=UserRole.user,
                password='KYx%i5M%O#rqrEaxU3latrO!oo#gRi5862YHvk!394roft',
                second_factor='3RCUMBK2KJY7YFPX453MWZHAOL4G74OP',
                tags=[
                    Tag(title='Daryl - Testtag1'),
                    Tag(title='Daryl - Testtag2')
                ],
                clients=[
                    APIClient(
                        expires=None,
                        user_id=2,
                        enabled=True,
                        app_name='RESTbook',
                        app_publisher='Tanha Kabir',
                        token='abcdefgh1234567890',
                        tokens=[
                            api_token_objects[0]
                        ]
                    )
                ],
                tokens=[
                    api_token_objects[0]
                ]
            )
        ]

        # Combine the data objects to create
        data = list()
        data += user_objects

        for entry in data:
            try:
                with DatabaseSession(commit_on_end=True, expire_on_commit=False) \
                        as session:

                    # Set the password (if this is a user)
                    if isinstance(entry, User):
                        entry.set_password(entry.password)

                    # Add the user to the database
                    logger.info(
                        f'Creating object "{entry}" and related objects')
                    session.add(entry)
            except (pymysql.err.IntegrityError, sqlalchemy.exc.IntegrityError) as e:
                logger.warning(f'IntegrityError: {str(e)}')

    # Done!
    logger.info('Script done')
