""" Module that creates the Flask Blueprint for the static frontend
    files of the My Ganymade service. """

from flask.blueprints import Blueprint

blueprint_static = Blueprint(
    name='my_ganymade_static',
    import_name=__name__,
    url_prefix='/'
)


@blueprint_static.route('/')
def index():
    return 'Static pages'
