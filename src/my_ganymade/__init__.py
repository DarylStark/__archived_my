""" The my_ganymade package is the frontend for the application. It is
    a VueJS application that is served using a Python Flask Application.
    This package contains the Flask application and the NodeJS files to
    create the VueJS frontend """
import logging
from config_loader import ConfigLoader
from flask import Flask
from rich.logging import RichHandler
from my_ganymade.exceptions import ConfigNotLoadedError
from my_ganymade.backend import blueprint_backend
from my_ganymade.static import blueprint_static

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

# Create a logger for the My Ganymade package
logger = logging.getLogger('MyGanymade')

# Create a Flask object
logger.debug('Creating Flask object')
flask_app = Flask(__name__)

# Register the blueprints for the data and the static pages
flask_app.register_blueprint(blueprint_backend)
flask_app.register_blueprint(blueprint_static)
