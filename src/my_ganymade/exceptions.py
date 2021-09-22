""" Exceptions for the 'my_ganymade' package. """


class MyGanymadeError(Exception):
    """ Base class for exception for Ganymade. """
    pass


class ConfigNotLoadedError(MyGanymadeError):
    """ Exception when the configuration couldn't be loaded. """
    pass
