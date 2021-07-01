"""
    The `my_database` package does all the database handling for the
    'My' application.
"""
from logging import getLogger
from config_loader import ConfigLoader
from database import Database
from my_database.exceptions import ConfigNotLoadedError

# Load the settings
if not ConfigLoader.load_settings():
    raise ConfigNotLoadedError(
        f'Configuration was not yet loaded.')

# Create a Logger
logger = getLogger('my_database')

# Get the database credentials
# TODO: retrieve this from the configuration
username = ConfigLoader.config['database']['username']
password = ConfigLoader.config['database']['password']
server = ConfigLoader.config['database']['server']
database = ConfigLoader.config['database']['database']

# Connect to the database and create the needed tables
connection_string = \
    f'mysql+pymysql://{username}:{password}@{server}/{database}'

Database.connect(
    connection=connection_string,
    create_tables=False
)
