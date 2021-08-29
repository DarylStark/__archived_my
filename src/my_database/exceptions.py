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


class IntegrityError(MyDatabaseError):
    """ Exception when a integrity error occurs. """
    pass


class PermissionDeniedError(MyDatabaseError):
    """ Exception that happens when the user tries to do something that
        the requesting user is not allowed to do. """
    pass


class NotFoundError(MyDatabaseError):
    """ Exception that happens when the user tries to change or delete
        a resource that doesn't exists. """
    pass


class FieldNotValidatedError(MyDatabaseError):
    """ Exception that happens when a user tries to use a value that is
        not aloud """
    pass
