""" Exceptions for the 'my_ganymede' package. """


class MyGanymedeError(Exception):
    """ Base class for exception for Ganymede. """
    pass


class ConfigNotLoadedError(MyGanymedeError):
    """ Exception when the configuration couldn't be loaded. """
    pass


class InvalidInputError(MyGanymedeError):
    """ Exception that occurs when the user gives invalid input. Sould
        be handled as HTTP 400 error. """
    pass
