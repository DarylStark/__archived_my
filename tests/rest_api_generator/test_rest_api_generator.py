"""
    This module defines unit tests for the RESTAPIGenerator
"""
# ---------------------------------------------------------------------
# Add include path. We need to do this because we are not in the
# original path
import sys
import os
from typing import List
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(
        __file__), os.path.pardir, os.path.pardir)) + '/src'
)
# ---------------------------------------------------------------------
# Imports
from rest_api_generator import RESTAPIGenerator, RESTAPIGroup, RESTAPIEndpointURL
# ---------------------------------------------------------------------


def test_api_group_registration() -> None:
    """ Unit test that creates a RESTAPIGenerator object, adds groups
        to it and endpoints, and checks if all the URLs are in there.
    """

    # Define the needed URLs:
    needed_urls: List = [
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

    # Retrieve a list of registered endpoints
    endpoints: List[RESTAPIEndpointURL] = rest_api.get_all_endpoints()

    # Check the length of the endpoints list, and verify that it is the
    # same length as our check list
    if len(endpoints) != len(needed_urls):
        assert False

    # Get the registered URLs
    registered_urls = [endpoint.url for endpoint in endpoints]

    # Check if all endpoints are in there
    for needed_url in needed_urls:
        if needed_url not in registered_urls:
            assert False

    # Done! Everything looks fine
    assert True
# ---------------------------------------------------------------------
