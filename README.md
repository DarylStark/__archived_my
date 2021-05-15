# The My Daryl Stark application

Services for the My application that will act as a personal assistant for Daryl Stark. The personal assistant will be repsonsible for a few tasks, which will grow to demand of Daryl Stark. For startes, it will be the backend for a Notepad application with REST API.

## Folder structure

The project is divided in a few directories:

```
.
├── .vscode
├── docs
├── env
├── src
│   ├── my_backend
│   └── my_rest_api_v1
├── tests
└── tools
```

### .vscode

The `.vscode` directory contains files that are needed for VScode to understand this repository. The `settings.json` defines the settings for the project. The `launch.json` contains the debug targets that can be used.

### /docs

This directory wil contain documentation about the project.

### env

_Warning: this directory is not included in the Git repository_

The `env` directory contains a virtual environment for the Python runtime. This directory is not included in the Git repo to keep the Git repo small. To create and activate a virtual environment, use the following command:

```bash
python3 -m venv env
source env/bin/activate
```

### /src

The _src_ directory will hold the source for the services for this version of the software. As of right now, there are three services:

#### _my_backend_

The backend will be responsible for to run long-running tasks like retrieving data online. It won't be callable by the end-user.

#### _my_rest_api_v1_

The REST API v1 package will be responsible to expose a REST API to the end user that he or she can use to create data in the application, update data, remove data and retrieve data. The API will be one of the most important parts of the application

###  /tests

The tests directory will contain the unit tests for the source code. In order to make sure a unit test works, it is imperative to include the path to the tests in the source code. This can be done as follows:

```python
import sys
sys.path.append('src')
```

For more information about unit testing, check the [Unit testing](#unit_testing) chapter of this README.

### /tools

The tools directory will contain scripts and tools to automate specific tasks that are neede during programming

## <a name="unit_testing"></a>Unit testing

The application will be written with unit testing in mind. To run automated testing, we use the `pytest` Python module. Within the `clients` and `services` directories is a `tests` directory. Within these directories we can create modules for tests.

### Naming convention

Modules with test methods and classes will begin with `test_`. Methods within these modules that are used for unit testing, will begin with `test_`. Classes within the modules that are used for unit testing, will begin with `Test`.

## Code quality

To make sure the code if of the highest quality possible, we demand that all Python code is written according to the [PEP-8 Style Guide for Python](https://www.python.org/dev/peps/pep-0008/). To make sure all code complies to this style guide, we use the `autopep8` package for Python. VScode can use this package to automatically format Python code.

As an addition to PEP-8, we will use type hinting as much as we can. To get more specific types, the `typing` package for Python can be used. As addition to this, we will use a docstring for all defined functions, classes, modules and packages. This is done so we can use a automated help system to generate code documentation.