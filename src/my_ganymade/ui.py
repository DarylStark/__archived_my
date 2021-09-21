""" Module that creates the Flask Blueprint for the UI pages of the
    application, like the login form and the dashboard page. """

from flask.blueprints import Blueprint
from typing import Optional
import jinja2

# Create a Jinja2 environment that the application can use to retrieve
# and parse templates
templateLoader = jinja2.FileSystemLoader(searchpath='my_ganymade/templates')
templateEnv = jinja2.Environment(loader=templateLoader)

# Create the blueprint for the UI pages
blueprint_ui = Blueprint(
    name='my_ganymade_ui',
    import_name=__name__,
    url_prefix='/ui/'
)


@blueprint_ui.route(
    '/',
    defaults={'path': None},
    methods=['GET']
)
@blueprint_ui.route(
    '/<path:path>',
    methods=['GET']
)
def dashboard(path: Optional[str]) -> str:
    """ Function for the 'Dashboard' page of the application. Every page
        that doesn't have a route in this blueprint gets redirected to
        this. The VueJS router will decide what to display. """

    # Open the correct template file
    template = templateEnv.get_template('dashboard.html')

    # Create a dict with the data for the template
    data = {
        'title': 'Dashboard',
        'body_js_files': ['dashboard.js']
    }

    # Render the template and return the value
    return template.render(data)


@blueprint_ui.route(
    '/login',
    methods=['GET']
)
def login() -> str:
    """ Function for the Login form of the application. """

    # Open the correct template file
    template = templateEnv.get_template('login.html')

    # Create a dict with the data for the template
    data = {
        'title': 'Login',
        'body_js_files': ['login.js']
    }

    # Render the template and return the value
    return template.render(data)
