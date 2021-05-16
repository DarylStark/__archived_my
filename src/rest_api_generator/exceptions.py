"""
    Exceptions for the 'rest_api_generator' package.
"""
# ---------------------------------------------------------------------


class RESTAPIGeneratorError(Exception):
    """ Base exception for RESTAPIGenerator-exceptions """
    pass


class RESTAPIGeneratorCriticalError(RESTAPIGeneratorError):
    """ Exception that should result in complete termination of the
        application """
    pass


class InvalidGroupError(RESTAPIGeneratorCriticalError):
    """ Error that happens when the database credentials are not
        correct """
    pass
# ---------------------------------------------------------------------
