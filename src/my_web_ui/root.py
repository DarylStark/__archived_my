""" Module that creates the Flask Blueprint for the root page of
    the application """

from flask.blueprints import Blueprint
from flask import redirect
from typing import Optional

# Create the blueprint for the UI pages
blueprint_root = Blueprint(
    name='my_web_ui_root',
    import_name=__name__,
    url_prefix='/'
)


@blueprint_root.route(
    '/',
    defaults={'path': None},
    methods=['GET']
)
def rootpage(path: Optional[str]) -> str:
    """ The root route for the app redirects the user to the `/ui`
        route """

    return redirect('/ui/')
