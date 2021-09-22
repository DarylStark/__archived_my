""" Script to copies the files in the NodeJS project to the my_ganymade
    static folder. """

import logging
import sys
import glob
import shutil
from os.path import isdir
from rich.logging import RichHandler

nodejs_path = './src/my_ganymade/nodejs-project'
my_ganymade_path = './src/my_ganymade/static'

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.DEBUG, format="%(message)s",
                        datefmt="[%X]", handlers=[RichHandler()])
    logger = logging.getLogger(name='database-create')

    # Find the 'nodejs-project' folder
    if isdir(nodejs_path):
        logger.info(f'Path "{nodejs_path}" exists')

        # This list of tuples contains the source and destination
        # directories for everything that should be copied
        copy = [
            (f'{nodejs_path}/dist/css', f'{my_ganymade_path}/css'),
            (f'{nodejs_path}/dist/js', f'{my_ganymade_path}/js'),
            (f'{nodejs_path}/dist/static/fonts', f'{my_ganymade_path}/fonts')
        ]

        # Copy the files
        for source, destination in copy:
            # Get all files in the source directory
            files = glob.glob(f'{source}/*')
            for file in files:
                logger.info(f'Copying file "{file}" to "{destination}"')
                shutil.copy(file, destination)
    else:
        logger.error(f'Path "{nodejs_path}" does not exist')
        sys.exit(1)
