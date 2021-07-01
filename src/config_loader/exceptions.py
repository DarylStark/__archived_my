"""
    Exceptions for the 'config_loader' package.
"""


class ConfigLoaderError(Exception):
    """ Base exception for ConfigLoader-exceptions. """
    pass


class EnvironmentAlreadySetError(ConfigLoaderError):
    """ Exception that occurs when the user tries to set the
        environment after it was already done. """
    pass


class EnvironmentNotSetError(ConfigLoaderError):
    """ Exception that occurs when the user tries to retrieve the
        config before configuring the environment. """
    pass


class ConfigFileNotFoundError(ConfigLoaderError):
    """ Exception that occurs when the configfile couldn't be found.
    """
    pass


class ConfigFileNotValidError(ConfigLoaderError):
    """ Exception that occurs when the configfile is invald. """
    pass
