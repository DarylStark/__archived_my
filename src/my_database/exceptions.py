"""
    Exceptions for the 'my_database' package.
"""


class MyDatabaseError(Exception):
    """ Base exception for MyDatabase-exceptions. """
    pass


class FilterNotValidError(MyDatabaseError):
    """ Exception that occurs when the user tries to filter on a wrong
        type. """
    pass


class ConfigNotLoadedError(MyDatabaseError):
    """ Exception when the configuration couldn't be loaded. """
    pass
