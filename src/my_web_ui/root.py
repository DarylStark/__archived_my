""" Module that creates the Flask Blueprint for the root page of
    the application """

import os
from typing import Optional

from flask import redirect, send_from_directory
from flask.blueprints import Blueprint

# Create the blueprint for the UI pages
blueprint_root = Blueprint(
    name='my_web_ui_root',
    import_name=__name__,
    url_prefix='/'
)


@blueprint_root.route(
    '/favicon.ico',
    methods=['GET']
)
def favicon() -> str:
    """ The favicon for the application """

    return send_from_directory(
        os.path.join(
            os.path.dirname(__file__),
            'static',
            'favicon'),
        'nerd-face.ico',
        mimetype='image/vnd.microsoft.icon')


@blueprint_root.route(
    '/',
    defaults={'path': None},
    methods=['GET']
)
def rootpage(path: Optional[str]) -> str:
    """ The root route for the app redirects the user to the `/ui`
        route """

    return redirect('/ui/')
