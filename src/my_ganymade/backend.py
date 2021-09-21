""" Module that creates the Flask Blueprint for the backend of the
    My Ganymade service. """

from flask.blueprints import Blueprint

blueprint_backend = Blueprint(
    name='my_ganymade_backend',
    import_name=__name__,
    url_prefix='/data/'
)


@blueprint_backend.route('/')
def index():
    return 'Backend homepage'
