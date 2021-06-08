"""
    The `my_database` package does all the database handling for the
    'My' application.
"""
# ---------------------------------------------------------------------
from os import environ
from database import Database
from logging import getLogger
# ---------------------------------------------------------------------
# TODO: Make this easier to configure

# Create a Logger
logger = getLogger('my_database')

# Get the database credentials
username = environ["DB_USERNAME"]
password = environ["DB_PASSWORD"]
server = environ["DB_SERVER"]
database = environ["DB_DATABASE"]

# Connect to the database and create the needed tables
connection_string = \
    f'mysql+pymysql://{username}:{password}@{server}/{database}'

Database.connect(
    connection=connection_string,
    create_tables=True
)
# ---------------------------------------------------------------------
