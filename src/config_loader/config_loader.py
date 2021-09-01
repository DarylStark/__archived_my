""" Module that contains the static 'ConfigLoader' class. This is a
    class with only class-methods. """

import collections
import os
import re
from logging import getLogger
from os import environ
from typing import Dict, Optional

import yaml
from yaml.scanner import ScannerError

from config_loader.exceptions import (ConfigFileNotFoundError,
                                      ConfigFileNotValidError,
                                      EnvironmentAlreadySetError,
                                      EnvironmentNotSetError)


class ConfigLoader:
    """ The ConfigLoader class enables the user to load configuration
        from a file. """

    # Class variable that contains the selected environment
    environment: Optional[str] = None

    # Class variable for the file that is going to be used
    yaml_file: Optional[str] = None

    # The actual config
    config: dict = dict()

    # Boolean that keeps track if the config is loaded
    is_loaded: bool = False

    @classmethod
    def set_file(cls, yaml_file: str) -> None:
        """ Method to set the YAML file.

            Parameters
            ----------
            yaml_file : str
                The YAML file to use

            Returns
            -------
            None
        """

        # Set the YAML file
        cls.yaml_file = yaml_file

    @classmethod
    def set_environment(cls, environment: str) -> None:
        """ Method to set the environment.

            Parameters
            ----------
            environment : str
                The environment to use (for example; production)

            Returns
            -------
            None
        """

        # Set the environment
        cls.environment = environment

    @classmethod
    def load_settings(cls, yaml_file: Optional[str] = None) -> bool:
        """ Method to load the settings into the application.

            Parameters
            ----------
            yaml_file : Optional[str] [default=None]
                The YAML file to retrieve the config from. If not set,
                the script wil try to get if from the environment. If
                that also doesn't work, it assumes 'config.yaml'.

            Returns
            -------
            bool
                True if the load succeeds, False if it doesn't.
        """

        if not cls.is_loaded:
            # First we determine the file to use.
            if yaml_file is not None:
                cls.yaml_file = yaml_file
            elif cls.yaml_file is None:
                if 'CONFIG_FILE' in environ.keys():
                    cls.yaml_file = environ['CONFIG_FILE']
                else:
                    cls.yaml_file = 'config.yaml'

            # Then, we search for the environment
            if cls.environment is None:
                if 'ENVIRONMENT' in environ.keys():
                    cls.environment = environ['ENVIRONMENT']
                else:
                    cls.environment = 'production'

            try:
                # Try to load the file
                with open(cls.yaml_file) as file_stream:
                    data = file_stream.read()
                cls.data = yaml.safe_load(data)

                # We can now merge the configurations. In the configuration
                # file should be a 'default' key. This key should contain
                # three settings:
                #
                # - environments: a list containing the possible
                #                 environments
                # - config: a object with the different settings
                #
                # Besides the 'default' key, a key for each environment can
                # exists. The settings in the object with the key that
                # matches the 'selected-environment'  will be used to
                # override the 'default' settings.

                selected_environment = cls.environment
                if cls.environment is None:
                    raise EnvironmentNotSetError('Environment is not set')

                cls.config = cls.data['default']['config']

                # Merge the selected environment (if this is defined)
                if selected_environment in cls.data.keys():
                    cls.merge_environment(
                        config=cls.config,
                        environment=cls.data[selected_environment]
                    )

                # Loop through the settings and replace all values that
                # contain a environment variable.
                cls.set_environment_variables(cls.config)
            except FileNotFoundError:
                # File does not exists
                raise ConfigFileNotFoundError(
                    f'File {cls.yaml_file} does not exist!')
            except (ScannerError, KeyError) as err:
                # File could not be decoded
                raise ConfigFileNotValidError(
                    f'Error while loading configfile "{cls.yaml_file}": {err}')

            # Everything went fine
            cls.is_loaded = True
            return True
        else:
            return True

    @classmethod
    def merge_environment(cls, config: dict, environment: dict) -> None:
        """ Method to merge the config of the selected environment
            into the configuration.

            Parameters
            ----------
            config : dict
                The configuration dict.

            environment : dict
                The environment to use

            Returns
            -------
            None
        """

        # Loop through the key/value paris
        for key in environment.keys():
            if key in config \
                    and isinstance(config[key], dict) \
                    and isinstance(environment[key], collections.Mapping):
                # Recursivly merge
                cls.merge_environment(config[key], environment[key])
            else:
                # Overwrite setting
                config[key] = environment[key]

    @classmethod
    def set_environment_variables(cls, config: dict) -> None:
        """ Method to replace all values that should be a environment
            variable.

            Parameters
            ----------
            config : dict
                The dict with the variables to replace.

            Returns
            -------
            None
        """

        def parse(value: re.Match) -> str:
            """ Method that does the actual parsing of a environment
                variable. """
            return environ[value.groups()[0]]

        for key, value in config.items():
            if type(value) is dict:
                # We recursively walk through the dict
                cls.set_environment_variables(value)
            elif type(value) is str:
                # Not a dict anymore, let's process the value
                config[key] = re.sub(
                    r"\$\{env:([a-zA-Z0-9_]+)\}",
                    parse,
                    value
                )
