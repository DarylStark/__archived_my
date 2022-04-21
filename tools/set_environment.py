""" Module that contains a method to set environment variables from a
    environment file.
"""

from logging import Logger
import sys
import os


def set_environment(environment_file: str, logger: Logger) -> None:
    """ Method that reads a environment file and sets the environment
        variables """

    # Open the file
    logger.info('Setting environment variables')
    try:
        with open(file=environment_file) as env_file:
            # Get all the lines and strip off the whitespace
            lines = [line.strip() for line in env_file.readlines()]
    except FileNotFoundError:
        logger.error(f'File "{environment_file}" not found')
        sys.exit(1)

    # Loop through the lines and retrieve the variable name and the
    # value
    for line in lines:
        try:
            # Retrieve the values
            variable_name, variable_value = line.split('=')

            # Set the variable
            os.environ[variable_name] = variable_value

            logger.info(f'Set variable {variable_name}')
        except ValueError:
            # The error was not correctly defined
            logger.warning(f'Line not compliant:\n> {line}')
