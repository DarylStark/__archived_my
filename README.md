# The My Daryl Stark application

This repository contains the services for the My application, which will act as a personal assistant for Daryl Stark. The personal assistant will be repsonsible for a few tasks, which will grow to demand of Daryl Stark. For starters, it will be the backend for a Notebook application with REST API.

## Folder structure

The project is divided in a few directories:

```
.
├── .environment
├── .vscode
├── docs
│   ├── code
│   ├── config_loader
│   ├── database
│   └── rest_api_generator
├── env
├── jenkins
├── src
│   ├── config_loader
│   ├── database
│   ├── my_database
│   ├── my_database_model
│   ├── my_rest_api_v1
│   └── rest_api_generator
├── tests
└── tools
```

### /.vscode

The `.vscode` directory contains files that are needed for VScode to work with this repository. The `settings.json` defines the settings for the project. The `launch.json` contains the debug targets that can be used. These files are created by Daryl Stark to use by Daryl Stark and should only be overwritten by Daryl Stark.

### /docs

This directory wil contain documentation about the project. There are a few subdirectories in this directory:

-   code
    -   Contains documentation about the code, like the style guide
-   config_loader
    -   Contains documentation about the Config Loader package
-   database
    -   Contains documentation about the database model for this application
-   rest_api_generator
    -   Contains documentation about the REST API Generator package

### /env

_Warning: this directory is not included in the Git repository_

The `env` directory contains a virtual environment for the Python runtime. This directory is not included in the Git repo to keep the Git repo small. To create and activate a virtual environment, use the following command:

```bash
python3 -m venv env
source env/bin/activate
```

After that, install the needed libraries with the following command:

```bash
pip3 install -r src/requirements.txt
```

### /src

The _src_ directory will hold the source for the services for this version of the software and the packages used by these services. The following packages are created:

-   `config_loader`
-   `database`
-   `my_database`
-   `my_database_model`
-   `rest_api_generator`

The following services are created:

-   `my_rest_api_v1`
-   `my_web_ui`

As convention, every package that starts with the prefix `my_` is created for the sole purpose of the My-application. The other packagers can be used as reusable components for other applications.

#### Package `config_loader`

The config_loader package is responsible to load application configuration from a YAML file. Extended docs are in the [docs/config_loader](docs/config_loader/00%20-%20ConfigLoader.md) folder.

#### Package `database`

The database package can be used to create a SQLalchemy connection to a SQL database in a modest way; it doesn't create too many connections and provides a Context Manager which can be used for database sessions. Extended docs are in the [docs/database](docs/database/00%20-%20Database.md) folder.

#### Pacakge `my_database`

Serves as the backend for the complete application and all services. This package contains functions to perform specific commands on the database, like created, retrieving, updating and deleting resources. This package relies heavily on the `database` package.

#### Package `my_database_model`

Contains the complete database schema for the My-application. This package uses the `database` package to define a database schema in a ORM fashion.

#### Package `rest_api_generator`

A reusable package to easily create a JSON based REST API using a Flask Blueprint. Extended docs are in [docs/rest_api_generator](docs/rest_api_generator/00%20-%20REST%20API%20Generator.md).

#### Service `my_rest_api_v1`

This service exposes a REST API that can be used to interact with the data in the application.

#### Service `my_web_ui`

This service exposes a Flask application with the frontend files from the `my_portal` [repository](https://github.com/DarylStark/my_portal).

###  /jenkins

This directory contains scripts for the Jenkins pipeline. It will install the application and run the unit tests. In the future, this might be expanded to more tasks to completly do CI/CD.

###  /tests

The tests directory will contain the unit tests for the source code. In order to make sure a unit test works, it is imperative to include the path to the tests in the source code. This can be done as follows:

```python
import sys
sys.path.append('src')
```

For more information about unit testing, check the [Unit testing](#unit_testing) chapter of this README.

### /tools

The tools directory will contain scripts and tools to automate specific tasks that are neede during programming. Right now, it contains one tool: `database-create.py`. This script can be used to (re-)create the database or it's data.

## <a name="unit_testing"></a>Unit testing

The application will be written with unit testing in mind. To run automated testing, we use the `pytest` Python module. Within the `clients` and `services` directories is a `tests` directory. Within these directories we can create modules for tests.

### Naming convention

Modules with test methods and classes will begin with `test_`. Methods within these modules that are used for unit testing, will begin with `test_`. Classes within the modules that are used for unit testing, will begin with `Test`.

## Code quality

To make sure the code if of the highest quality possible, we demand that all Python code is written according to the [PEP-8 Style Guide for Python](https://www.python.org/dev/peps/pep-0008/). To make sure all code complies to this style guide, we use the `autopep8` package for Python. VScode can use this package to automatically format Python code.

As an addition to PEP-8, we will use type hinting as much as we can. To get more specific types, the `typing` package for Python can be used. As addition to this, we will use a docstring for all defined functions, classes, modules and packages. This is done so we can use a automated help system to generate code documentation.
