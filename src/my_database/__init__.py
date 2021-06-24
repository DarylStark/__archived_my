"""
    The `my_database` package does all the database handling for the
    'My' application.
"""
# ---------------------------------------------------------------------
from os import environ
from database import Database
from logging import getLogger
from config_loader import ConfigLoader
from my_database.exceptions import ConfigNotLoadedError, \
    EnvironmentNotSetError
# ---------------------------------------------------------------------
# Get the environment we are one
if 'MY_ENVIRONMENT' in environ.keys():
    environment = environ['MY_ENVIRONMENT']
else:
    raise EnvironmentNotSetError(
        'Environment not set: please set the environment with the ' +
        'MY_ENVIRONMENT env')

# Load the settings
ConfigLoader.init(environment='production')
if not ConfigLoader.load_settings(None):
    raise ConfigNotLoadedError(
        f'Config could not be loaded from file "{ConfigLoader.yaml_file}"')

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
# ---------------------------------------------------------------------
