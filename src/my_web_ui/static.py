""" Module that creates the Flask Blueprint for the static frontend
    files of the My Web UI service. This Blueprint is only here to
    serve static files and does not contain any Flask-routed functions.
"""

from flask.blueprints import Blueprint

blueprint_static = Blueprint(
    name='my_web_ui_static',
    import_name=__name__,
    url_prefix='/static/',
    static_folder='my_web_ui/static/',
    static_url_path='/'
)
