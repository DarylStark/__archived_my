"""
    This module defines unit tests for the RESTAPIGenerator
"""
# ---------------------------------------------------------------------
# Add include path. We need to do this because we are not in the
# original path
import sys
import os
import pytest
from typing import List
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(
        __file__), os.path.pardir, os.path.pardir)) + '/src'
)
# ---------------------------------------------------------------------
# Imports
from rest_api_generator import RESTAPIGenerator, RESTAPIGroup, RESTAPIEndpointURL
# ---------------------------------------------------------------------
# Fixtures


@pytest.fixture
def fixture_rest_api() -> RESTAPIGenerator:
    """ Fixture to set up a RESTAPIGenerator object with a few groups
        registered and endpoints connected. """

    # Create a RESTAPIGenerator object
    rest_api = RESTAPIGenerator('rest_api_unittest')

    # Create groups
    group_a = RESTAPIGroup('group_a')
    group_b = RESTAPIGroup('group_b')
    group_c = RESTAPIGroup('group_c')
    group_d = RESTAPIGroup('group_d')

    # Add groups to the API object
    rest_api.register_group(group_a)
    rest_api.register_group(group_b)
    rest_api.register_group(group_c)
    rest_api.register_group(group_d)

    # Add endpoint to the groups
    @group_a.register_endpoint(['endpoint_1', 'endpoint_1/'])
    def group_a_endpoint_1(self):
        pass

    @group_a.register_endpoint(['endpoint_2', 'endpoint_2/'])
    def group_a_endpoint_2(self):
        pass

    @group_b.register_endpoint(['endpoint_1', 'endpoint_1/'])
    def group_b_endpoint_1(self):
        pass

    @group_b.register_endpoint(['endpoint_2', 'endpoint_2/'])
    def group_b_endpoint_2(self):
        pass

    @group_c.register_endpoint(['endpoint_1', 'endpoint_1/'])
    def group_c_endpoint_1(self):
        pass

    @group_c.register_endpoint(['endpoint_2', 'endpoint_2/'])
    def group_c_endpoint_2(self):
        pass

    @group_d.register_endpoint(['endpoint_1', 'endpoint_1/'])
    def group_d_endpoint_1(self):
        pass

    @group_d.register_endpoint(['endpoint_2', 'endpoint_2/'])
    def group_d_endpoint_2(self):
        pass

    # Return the created object
    return rest_api


@pytest.fixture
def fixture_expected_urls() -> List[str]:
    """ Fixture to create a list of expected URLs """

    return [
        'group_a/endpoint_1',
        'group_a/endpoint_2',
        'group_b/endpoint_1',
        'group_b/endpoint_2',
        'group_c/endpoint_1',
        'group_c/endpoint_2',
        'group_d/endpoint_1',
        'group_d/endpoint_2',
        'group_a/endpoint_1/',
        'group_a/endpoint_2/',
        'group_b/endpoint_1/',
        'group_b/endpoint_2/',
        'group_c/endpoint_1/',
        'group_c/endpoint_2/',
        'group_d/endpoint_1/',
        'group_d/endpoint_2/'
    ]

# ---------------------------------------------------------------------
# Tests


def test_api_group_registered_urls(fixture_rest_api, fixture_expected_urls) -> None:
    """ Unit test for registered URLs

        Check if all expected URLs are in the URL list for a specific
        RESTAPIGenerator object.
    """

    # Retrieve a list of registered endpoints
    endpoints: List[RESTAPIEndpointURL] = fixture_rest_api.get_all_endpoints()

    # Get the registered URLs
    registered_urls = [endpoint.url for endpoint in endpoints]

    # Check if all endpoints are in there
    for needed_url in fixture_expected_urls:
        if needed_url not in registered_urls:
            assert False

    # Done! Everything looks fine
    assert True


def test_api_group_registered_urls_length(fixture_rest_api, fixture_expected_urls) -> None:
    """ Unit test for registered URLs

        Check if the lenght of expected URLs and the length of the URL
        list in a RESTAPIGenerator object are equal.
    """

    # Retrieve a list of registered endpoints
    endpoints: List[RESTAPIEndpointURL] = fixture_rest_api.get_all_endpoints()

    # Check the length of the endpoints list, and verify that it is the
    # same length as our check list
    if len(endpoints) != len(fixture_expected_urls):
        assert False

    # Done! Everything looks fine
    assert True
# ---------------------------------------------------------------------
