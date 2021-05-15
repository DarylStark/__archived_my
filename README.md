# My

Application that will act as a personal assistant for Daryl Stark.

# Folder structure

The project is divided in a few directories:

```
.
└── src
    ├── clients
    │   └── tests
    └── services
        ├── my_backend
        ├── my_oauth
        ├── my_rest_api_v1
        └── tests
```

## Clients

The _clients_ directory will hold the source code for clients for this version of the software. For now, no clients are defined.

###  Tests

The tests directory will contain the unit tests for the clients.

## Services

The _services_ directory will hold the source for services for this version of the software. As of right now, there are three services:

-   backend
    -   Definfed in the Python package my_backend
-   oatuh
    -   Definfed in the Python package my_oauth
-   rest_api_v1
    -   Definfed in the Python package my_rest_api_v1

###  Tests

The tests directory will contain the unit tests for the services.

# Unit testing

The application will be written with unit testing in mind. To run automated testing, we use the `pytest` Python module. Within the `clients` and `services` directories is a `tests` directory. Within these directories we can create modules for tests.

## Naming convention

Modules with test methods and classes will begin with `test_`. Methods within these modules that are used for unit testing, will begin with `test_`. Classes within the modules that are used for unit testing, will begin with `Test`.

# Code quality

To make sure the code if of the highest quality possible, we demand that all Python code is written according to the [PEP-8 Style Guide for Python](https://www.python.org/dev/peps/pep-0008/). To make sure all code complies to this style guide, we use the `autopep8` package for Python. VScode can use this package to automatically format Python code.

As an addition to PEP-8, we will use type hinting as much as we can. To get more specific types, the `typing` package for Python can be used. As addition to this, we will use a docstring for all defined functions, classes, modules and packages. This is done so we can use a automated help system to generate code documentation.