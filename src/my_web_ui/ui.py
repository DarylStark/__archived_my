""" Module that creates the Flask Blueprint for the UI pages of the
    application, like the login form and the dashboard page. """

from flask.blueprints import Blueprint
from flask import redirect, Response
from typing import Optional, Union
import jinja2
from my_web_ui.authentication import get_active_user_session

# Create a Jinja2 environment that the application can use to retrieve
# and parse templates
templateLoader = jinja2.FileSystemLoader(searchpath='my_web_ui/templates')
templateEnv = jinja2.Environment(loader=templateLoader)

# Create the blueprint for the UI pages
blueprint_ui = Blueprint(
    name='my_web_ui_ui',
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

    # Get the logged in user
    user_session = get_active_user_session()
    user_object = None

    if user_session is not None:
        user_object = user_session.user

    # Check if there is a logged on user
    if user_object is None:
        # Abort the request
        return redirect('/ui/login')

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
def login() -> Union[str, Response]:
    """ Function for the Login form of the application. """

    # Get the logged in user
    user_session = get_active_user_session()
    user_object = None

    if user_session is not None:
        user_object = user_session.user

    # Check if there is not logged on user. If there is, we redirect
    # the user to the dashboard
    if user_object is not None:
        # Abort the request
        return redirect('/ui/')

    # Open the correct template file
    template = templateEnv.get_template('login.html')

    # Create a dict with the data for the template
    data = {
        'title': 'Login',
        'body_js_files': ['login.js']
    }

    # Render the template and return the value
    return template.render(data)
