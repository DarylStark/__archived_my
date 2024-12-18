""" The my_web_ui package is the frontend for the application. It is
    a VueJS application that is served using a Python Flask Application.
    This package contains the Flask application and the NodeJS files to
    create the VueJS frontend """
from datetime import timedelta
import logging
import flask

import werkzeug.exceptions
from flask import Flask
from rich.logging import RichHandler

from config_loader import ConfigLoader
from my_web_ui.data_aaa import blueprint_data_aaa
from my_web_ui.data_api_clients import blueprint_data_api_clients
from my_web_ui.data_api_tokens import blueprint_data_api_tokens
from my_web_ui.data_dashboard import blueprint_data_dashboard
from my_web_ui.data_tags import blueprint_data_tags
from my_web_ui.data_user_account import blueprint_data_user_account
from my_web_ui.data_user_session import blueprint_data_user_sessions
from my_web_ui.data_web_ui_settings import blueprint_data_web_ui_settings
from my_web_ui.exceptions import ConfigNotLoadedError
from my_web_ui.root import blueprint_root
from my_web_ui.static import blueprint_static
from my_web_ui.ui import blueprint_ui, error_page

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

# Create a logger for the My MyWebUI package
logger = logging.getLogger('MyWebUI')

# Create a Flask object
logger.debug('Creating Flask object')
flask_app = Flask(__name__)

# Register error handler
flask_app.register_error_handler(werkzeug.exceptions.HTTPException, error_page)

# Set the Flask secret. This is used for session later on
flask_app.secret_key = ConfigLoader.config['flask']['secret']

# Configure session settings
flask_app.permanent_session_lifetime = timedelta(
    days=ConfigLoader.config['flask']['session_lifetime_days'])

# Register the blueprints for the data. This is basically the backend
# for the application.
flask_app.register_blueprint(blueprint_data_aaa)
flask_app.register_blueprint(blueprint_data_api_clients)
flask_app.register_blueprint(blueprint_data_api_tokens)
flask_app.register_blueprint(blueprint_data_dashboard)
flask_app.register_blueprint(blueprint_data_user_sessions)
flask_app.register_blueprint(blueprint_data_user_account)
flask_app.register_blueprint(blueprint_data_web_ui_settings)
flask_app.register_blueprint(blueprint_data_tags)

# Register the blueprints for the static files like the CSS, Javascript
# and images and one for the real UI.
flask_app.register_blueprint(blueprint_static)
flask_app.register_blueprint(blueprint_ui)
flask_app.register_blueprint(blueprint_root)
