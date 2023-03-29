"""
    Script to deploy the complete app or one of the services to
    Google App Engine
"""

import argparse
import logging
import os
import jinja2
import subprocess
from rich.logging import RichHandler
from set_environment import set_environment
from datetime import date

# Services that can be deployed
# TODO: Place this in a config.yaml file
gcloud_configuration = {
    'project': 'my-dstark-nl'
}
services = {
    'my_web_ui': {
        'runtime': 'python311',
        'instance_class': 'F1',
        'service_name': 'default',
        'version': '1-1-0',
        'environment': 'production',
        'min_instances': 0,
        'max_instances': 1
    },
    'my_rest_api_v1': {
        'runtime': 'python311',
        'instance_class': 'F1',
        'service_name': 'my-rest-api-v1',
        'version': '1-0-0',
        'environment': 'production',
        'min_instances': 0,
        'max_instances': 1
    }
}

if __name__ == '__main__':
    # Parse the arguments for the script
    parser = argparse.ArgumentParser(
        description='Deploy the app to Google App Engine')
    parser.add_argument('service',
                        metavar='service',
                        type=str,
                        help='The service to deploy',
                        choices=services.keys())
    parser.add_argument('--environment_file',
                        metavar='environment_file',
                        type=str,
                        help='A environment file with the settings')

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(level=logging.DEBUG, format="%(message)s",
                        datefmt="[%X]", handlers=[RichHandler()])
    logger = logging.getLogger(name='deploy-to-gae')

    logger.info('Starting the deployment to Google App Engine')

    # Set the environment
    if args.environment_file:
        logger.info('Importing environment')
        set_environment(args.environment_file, logger)

    # Create the `service.yaml` file
    template_loader = jinja2.FileSystemLoader(
        searchpath='./tools/gae-templates')
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template('service.yaml.j2')

    # Create the data for the template
    template_data = {
        **services[args.service],
        'service': args.service,
        'db_username': os.environ['DB_USERNAME'],
        'db_password': os.environ['DB_PASSWORD'],
        'db_server': os.environ['DB_SERVER'],
        'db_database': os.environ['DB_DATABASE'],
        'flask_secret': os.environ['FLASK_SECRET']
    }

    # Render the template
    logger.info('Rendering service file')
    yaml_file_contents = template.render(template_data)

    # Save the YAML file
    service_filename = f'service.{args.service}.yaml'
    logger.info(f'Saving service file: {service_filename}')
    with open(f'./src/{service_filename}', 'w') as yaml_output:
        yaml_output.write(yaml_file_contents)

    # Configure the `glcoud` CLI command
    # TODO: retrieve the current project so we can restore it
    logger.info('Setting project in Google Cloud CLI')
    process = subprocess.Popen(
        ['gcloud', 'config', 'set', 'project', gcloud_configuration["project"]],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    logger.info(f'Command output: {stderr}')

    # Calculate the versionname
    today = date.today()
    version = f'{today.year}{today.month:02}{today.day:02}--{services[args.service]["version"]}'

    # Deploy the app
    os.chdir('./src')
    logger.info(f'Deploying the service "{args.service}"')
    process = subprocess.Popen(
        ['gcloud', 'app', 'deploy', service_filename,
            '--quiet', '--version', version],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    logger.info(f'Command output: {stderr}')

    # Remove the created file
    logger.info(f'Removing created service file')
    os.remove(service_filename)
