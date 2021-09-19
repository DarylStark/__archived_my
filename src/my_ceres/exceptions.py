""" Exceptions for the 'my_ceres' package. """


class MyCeresError(Exception):
    """ Base class for exception for Ceres. """
    pass


class ConfigNotLoadedError(MyCeresError):
    """ Exception when the configuration couldn't be loaded. """
    pass
