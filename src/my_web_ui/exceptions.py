""" Exceptions for the 'my_web_ui' package. """


class MyWebUIError(Exception):
    """ Base class for exception for Web UI. """
    pass


class ConfigNotLoadedError(MyWebUIError):
    """ Exception when the configuration couldn't be loaded. """
    pass


class InvalidInputError(MyWebUIError):
    """ Exception that occurs when the user gives invalid input. Sould
        be handled as HTTP 400 error. """
    pass


class PermissionDeniedError(MyWebUIError):
    """ Exception that occurs when the user gives invalid input. Sould
        be handled as HTTP 400 error. """
    pass


class ResourceIntegrityError(MyWebUIError):
    """ Exception that occurs when the user adds, changes or deletes 
        something that generates a integrity error. Should be handled
        as HTTP 409 Error """
    pass


class ResourceNotFoundError(MyWebUIError):
    """ Exception that occurs when the user tries to retrieve a resource
        that doesn't exist. Should be handled as HTTP 404 error."""
    pass


class ServerError(MyWebUIError):
    """ Exception that occurs when something goes wrong on the server. Should
        be handled as HTTP 500 error. """
    pass
