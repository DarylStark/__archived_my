""" Script to copy the files in the NodeJS project to the my_ganymede
    static folder. """

import argparse
import glob
import logging
import os
import shutil
import sys
from os.path import isdir, isfile
from rich.logging import RichHandler
from set_environment import set_environment

if __name__ == '__main__':
    # Parse the arguments for the script
    parser = argparse.ArgumentParser(description='Create the database')
    parser.add_argument('environment_file',
                        metavar='environment_file',
                        type=str,
                        help='The environment file with the settings')

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(level=logging.DEBUG, format="%(message)s",
                        datefmt="[%X]", handlers=[RichHandler()])
    logger = logging.getLogger(name='install-ganymade-static-files')

    # Set the environment
    set_environment(args.environment_file, logger)

    if 'NODEJS_DIST_FOLDER' not in os.environ.keys():
        logger.critical('NODEJS_DIST_FOLDER environment variable not defined!')
        sys.exit(1)

    nodejs_path = os.environ['NODEJS_DIST_FOLDER']
    my_ganymede_path = './src/my_ganymede/static'

    # Find the 'nodejs-project' folder
    if isdir(nodejs_path):
        logger.info(f'Path "{nodejs_path}" exists')

        # This list of tuples contains the source and destination
        # directories for everything that should be copied
        copy = [
            (f'{nodejs_path}/css', f'{my_ganymede_path}/css'),
            (f'{nodejs_path}/js', f'{my_ganymede_path}/js'),
            (f'{nodejs_path}/static/fonts', f'{my_ganymede_path}/fonts')
        ]

        # Copy the files
        for source, destination in copy:
            # Get all files in the source directory
            files = glob.glob(f'{source}/*')
            for file in files:
                if isfile(file) and not '.map' in file:
                    logger.info(f'Copying file "{file}" to "{destination}"')
                    shutil.copy(file, destination)
    else:
        logger.error(f'Path "{nodejs_path}" does not exist')
        sys.exit(1)
