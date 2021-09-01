""" Exceptions for the 'rest_api_generator' package. """


class RESTAPIGeneratorError(Exception):
    """ Base exception for RESTAPIGenerator-exceptions. """
    pass


class RESTAPIGeneratorCriticalError(RESTAPIGeneratorError):
    """ Exception that should result in complete termination of the
        application. """
    pass


class RESTAPIGeneratorEndpointError(Exception):
    """ Base exception for exceptions that endpoints can throw """
    pass


class InvalidGroupError(RESTAPIGeneratorCriticalError):
    """ Error that happens when the programmer tries to add a invalid
        group to the generator. """
    pass


class UnauthorizedForResourceError(RESTAPIGeneratorEndpointError):
    """ Exception that indicates that a user is trying to access a
        resource that he or she has no permissions to. Should be
        handled as HTTP 401 error. """
    pass


class ResourceForbiddenError(RESTAPIGeneratorEndpointError):
    """ Exception that indicates that a user is trying to access a
        forbidden resource. Should be handled as HTTP 403 error. """
    pass


class ResourceNotFoundError(RESTAPIGeneratorEndpointError):
    """ Exception that indicates that a resoure is not found. Should be
        handled as HTTP 404 error. """
    pass


class ResourceIntegrityError(RESTAPIGeneratorEndpointError):
    """ Exception that indicates that a integrity error occurred.
        Should be handled as HTTP 500 error """
    pass


class ServerError(RESTAPIGeneratorEndpointError):
    """ Exception for server errors. Should be handled as HTTP 500
        error. """
    pass


class InvalidInputError(RESTAPIGeneratorEndpointError):
    """ Exception that occurs when the user gives invalid input. Sould
        be handled as HTTP 400 error. """
    pass
