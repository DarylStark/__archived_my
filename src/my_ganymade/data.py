""" Module that creates the Flask Blueprint for the data of the My
    Ganymade service. This is the backend for the My Ganymade service.
"""

from flask.blueprints import Blueprint

blueprint_data = Blueprint(
    name='my_ganymade_backend',
    import_name=__name__,
    url_prefix='/data/'
)


@blueprint_data.route(
    '/',
    methods=['GET']
)
def index() -> str:
    """ Homepage for the 'data' part of the application. """
    return 'Data homepage'
