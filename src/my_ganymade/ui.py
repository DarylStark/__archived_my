""" Module that creates the Flask Blueprint for the UI pages of the
    application, like the login form and the dashboard page. """

from flask.blueprints import Blueprint
from typing import Optional

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
    return f'UI homepage (Dashboard). Given path: "{path}"'


@blueprint_ui.route(
    '/login',
    methods=['GET']
)
def login() -> str:
    """ Function for the Login form of the application. """
    return 'UI homepage (Login)'
