""" Module that creates the Flask Blueprint for the static frontend
    files of the My Ganymede service. This Blueprint is only here to
    serve static files and does not contain any Flask-routed functions.
"""

from flask.blueprints import Blueprint

blueprint_static = Blueprint(
    name='my_ganymede_static',
    import_name=__name__,
    url_prefix='/static/',
    static_folder='my_ganymage/static/',
    static_url_path='/'
)
