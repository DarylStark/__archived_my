"""
    Script to create the missing tables from the database
"""
# ---------------------------------------------------------------------
# Add include path. We need to do this because we are not in the
# original path
import sys
import os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(
        __file__), os.path.pardir)) + '/src'
)
# ---------------------------------------------------------------------
# Imports
import argparse
import logging
import pymysql
import sqlalchemy
from rich.logging import RichHandler
from database import Database, DatabaseSession
from database.exceptions import DatabaseConnectionError
from database_my_model import *
# ---------------------------------------------------------------------
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

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(level=logging.DEBUG, format="%(message)s",
                        datefmt="[%X]", handlers=[RichHandler()])
    logger = logging.getLogger(name='database-create')

    # Open the file
    logger.info('Setting environment variables')
    try:
        with open(file=args.environment_file) as env_file:
            # Get all the lines and strip off the whitespace
            lines = [line.strip() for line in env_file.readlines()]
    except FileNotFoundError:
        logging.error(f'File "{args.environment_file}" not found')
        sys.exit(1)

    # Loop through the lines and retrieve the variable name and the
    # value
    for line in lines:
        try:
            # Retrieve the values
            variable_name, variable_value = line.split('=')

            # Set the variable
            os.environ[variable_name] = variable_value

            logger.info(f'Setted variable {variable_name}')
        except ValueError:
            # The error was not correctly defined
            logger.warning(f'Line not compliant:\n> {line}')

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
            create_tables=True
        )
    except DatabaseConnectionError:
        logger.critical('Couldn\'t connect to the database!')
        sys.exit(1)

    # Add test data
    if args.create_data:
        try:
            with DatabaseSession(commit_on_end=True, expire_on_commit=False) \
                    as session:

                # Create a new user-object and set the password
                new_user = User(fullname='Daryl Stark',
                                username='daryl.stark',
                                email='daryl@dstark.nl'
                                )
                new_user.set_password('test')

                # Add the user to the database
                logger.info(f'Creating user "{new_user.fullname}"')
                session.add(new_user)
        except (pymysql.err.IntegrityError, sqlalchemy.exc.IntegrityError):
            logger.warning('User not added; already in the database')

        try:
            with DatabaseSession(commit_on_end=True, expire_on_commit=False) \
                    as session:

                # Create a new APIClient-object
                new_client = APIClient(
                    expires=None,
                    created_by_user=1,
                    enabled=True,
                    app_name='Thunder Client',
                    app_publisher='Ranga Vadhineni',
                    token='abcdefgh1234567890'
                )

                # Add the user to the database
                logger.info(f'Creating API client "{new_client.app_name}"')
                session.add(new_client)
        except (pymysql.err.IntegrityError, sqlalchemy.exc.IntegrityError):
            logger.warning('API client not added; already in the database')

    # Done!
    logger.info('Script done')
# ---------------------------------------------------------------------
