"""
    Exceptions for the 'my_rest_api_v1' package.
"""


class MyRestAPIv1Error(Exception):
    """ Base class for exception for REST API v1. """
    pass


class EnvironmentNotSetError(MyRestAPIv1Error):
    """ Exception when the environment is not set via environment
        variabled. """
    pass


class ConfigNotLoadedError(MyRestAPIv1Error):
    """ Exception when the configuration couldn't be loaded. """
    pass
