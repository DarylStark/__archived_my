""" The my_ceres package is the frontend for the application. It is a
    VueJS application that is served using a Python Flask Application.
    This package contains the Flask application and the NodeJS files to
    create the VueJS frontend """
import logging
from config_loader import ConfigLoader
from flask import Flask
from rich.logging import RichHandler
from my_ceres.exceptions import ConfigNotLoadedError

# Load the settings
if not ConfigLoader.load_settings():
    raise ConfigNotLoadedError(
        f'Configuration was not yet loaded.')

# Configure logging
logging.basicConfig(
    level=ConfigLoader.config['logging']['level'],
    format='%(name)s: %(message)s',
    datefmt="[%X]",
    handlers=[RichHandler()]
)

# Create a logger for the My Ceres package
logger = logging.getLogger('MyCeres')

# Create a Flask object
logger.debug('Creating Flask object')
flask_app = Flask(__name__)


@flask_app.route('/')
def index():
    return 'Welcome to Ceres!'
