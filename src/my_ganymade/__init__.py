""" The my_ganymade package is the frontend for the application. It is
    a VueJS application that is served using a Python Flask Application.
    This package contains the Flask application and the NodeJS files to
    create the VueJS frontend """
import logging
from config_loader import ConfigLoader
from flask import Flask
from rich.logging import RichHandler
from my_ganymade.exceptions import ConfigNotLoadedError
from my_ganymade.data_aaa import blueprint_data_aaa
from my_ganymade.static import blueprint_static
from my_ganymade.ui import blueprint_ui

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

# Register the blueprints for the data. This is basically the backend
# for the application.
flask_app.register_blueprint(blueprint_data_aaa)

# Register the blueprints for the static files like the CSS, Javascript
# and images and one for the real UI.
flask_app.register_blueprint(blueprint_static)
flask_app.register_blueprint(blueprint_ui)
