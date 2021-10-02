""" Exceptions for the 'my_ganymade' package. """


class MyGanymadeError(Exception):
    """ Base class for exception for Ganymade. """
    pass


class ConfigNotLoadedError(MyGanymadeError):
    """ Exception when the configuration couldn't be loaded. """
    pass


class InvalidInputError(MyGanymadeError):
    """ Exception that occurs when the user gives invalid input. Sould
        be handled as HTTP 400 error. """
    pass
