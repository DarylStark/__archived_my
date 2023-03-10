""" The `my_database` package does all the database handling for the
    'My' application. """

from logging import getLogger

from config_loader import ConfigLoader
from database import Database
from my_database.exceptions import ConfigNotLoadedError
from my_database.validate_input import validate_input
from my_database_model import *

# Load the settings
if not ConfigLoader.load_settings():
    raise ConfigNotLoadedError(
        f'Configuration was not yet loaded.')

# Create a Logger
logger = getLogger('my_database')

# Get the database credentials
username = ConfigLoader.config['database']['username']
password = ConfigLoader.config['database']['password']
server = ConfigLoader.config['database']['server']
database = ConfigLoader.config['database']['database']
create_tables = ConfigLoader.config['sql_alchemy']['create_tables']

# Connect to the database and create the needed tables
connection_string = \
    f'mysql+pymysql://{username}:{password}@{server}/{database}'

Database.connect(
    connection=connection_string,
    create_tables=create_tables
)
