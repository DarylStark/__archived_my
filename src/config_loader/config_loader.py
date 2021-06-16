"""
    Module that contains the static 'ConfigLoader' class. This class
    be used to load configuration for the application.
"""
# ---------------------------------------------------------------------
# Imports
from os import environ
import os
from typing import Dict, Optional
import yaml
import collections
from logging import getLogger
from yaml.scanner import ScannerError
import re
# ---------------------------------------------------------------------


class ConfigLoader:
    """ The ConfigLoader class enables the user to load configuration
        from a file. """

    # Class variable that contains a dict with all created ConfigLoader
    # objects
    created_loaders = dict()

    @classmethod
    def get_config_loader(cls, yaml_file: Optional[str] = None) -> 'ConfigLoader':
        """ Method that can and should be used to retrieve a
            ConfigLoader object. """

        # The user can set the config file in a few ways; he can
        # specify it using the argument of this constructor or via the
        # environment variable 'CONFIG_FILE'. If neither is set, the
        # package will assume 'config.yaml'.
        if yaml_file:
            yaml_file = yaml_file
        else:
            yaml_file = 'config.yaml'
            if 'CONFIG_FILE' in environ.keys():
                yaml_file = environ['CONFIG_FILE']

        # Make sure we have the full filename
        full_filename = os.path.abspath(yaml_file)

        # Search if there is already a ConfigLoader object for this
        # file.
        if full_filename not in cls.created_loaders.keys():
            # Object doesn't exist yet, create one
            cls.created_loaders[full_filename] = ConfigLoader(
                yaml_file=full_filename
            )

        # Return the object
        return cls.created_loaders[full_filename]

    def __init__(self, yaml_file: str) -> None:
        """ The initializer sets the default values. """
        self.logger = getLogger('ConfigLoader')
        self.logger.debug(f'ConfigLoader created for file: {yaml_file}')
        self.yaml_file = yaml_file
        self.config = Optional[Dict]

    def load_settings(self, environment: Optional[str]) -> bool:
        """ Method to load the settings into the application. """

        try:
            # Try to load the file
            self.logger.debug(f'Loading file: {self.yaml_file}')
            data = ''
            with open(self.yaml_file) as file_stream:
                self.logger.debug(
                    'Opened file, retrieving contents')
                data = file_stream.read()

            self.logger.debug('Opened file. Loading it.')
            self.data = yaml.safe_load(data)

            # File loaded succesfully
            self.logger.debug('File is valid')

            # We can now merge the configurations. In the configuration
            # file should be a 'default' key. This key should contain
            # three settings:
            #
            # - environments: a list containing the possible
            #                 environments
            # - selected-environment: the environment to use
            # - config: a object with the different settings
            #
            # Besides the 'default' key, a key for each environment can
            # exists. The settings in the object with the key that
            # matches the 'selected-environment'  will be used to
            # override the 'default' settings.

            if not environment:
                selected_environment = \
                    self.data['default']['selected-environment']
            else:
                selected_environment = environment

            self.logger.debug(f'Selected environment: {selected_environment}')
            self.config = self.data['default']['config']

            # Merge the selected environment (if this is defined)
            self.logger.debug('Merging configuration')
            if selected_environment in self.data.keys():
                self.merge_environment(
                    config=self.config,
                    environment=self.data[selected_environment]
                )

            # Loop through the settings and replace all values that
            # contain a environment variable.
            self.set_environment_variables(self.config)
        except FileNotFoundError:
            # File does not exists
            self.logger.error(f'File {self.yaml_file} does not exist!')
            return False
        except (ScannerError, KeyError) as e:
            # File could not be decoded
            self.logger.error(
                f'Error while loading configfile "{self.yaml_file}": {e}')
            return False

        # Everything went fine
        return True

    def merge_environment(self, config: dict, environment: dict):
        """ Method to merge the config of the selected environment
            into the configuration. """

        # Loop through the key/value paris
        for key in environment.keys():
            if key in config \
                    and isinstance(config[key], dict) \
                    and isinstance(environment[key], collections.Mapping):
                # Recursivly merge
                self.merge_environment(config[key], environment[key])
            else:
                # Overwrite setting
                config[key] = environment[key]

    def set_environment_variables(self, config: dict) -> None:
        """ Method to replace all values that should be a environment
            variable. """

        def parse(value):
            """ Method that does the actual parsing of a environment
                variable. """
            return environ[value.groups()[0]]

        for key, value in config.items():
            if type(value) is dict:
                # We recursively walk through the dict
                self.set_environment_variables(value)
            elif type(value) is str:
                # Not a dict anymore, let's process the value
                config[key] = re.sub(
                    r"\$\{env:([a-zA-Z0-9_]+)\}",
                    parse,
                    value
                )
# ---------------------------------------------------------------------
