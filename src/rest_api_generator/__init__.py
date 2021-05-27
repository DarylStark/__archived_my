"""
    The api_generator package can be used to create a REST API for
    Flask by using classes to specify a API group.
"""
# ---------------------------------------------------------------------
# Imports
from rest_api_generator.rest_api_generator import RESTAPIGenerator
from rest_api_generator.rest_api_endpoint import RESTAPIEndpoint
from rest_api_generator.rest_api_group import RESTAPIGroup
from rest_api_generator.rest_api_endpoint_url import RESTAPIEndpointURL
from rest_api_generator.rest_api_authorization import RESTAPIAuthorization
from rest_api_generator.rest_api_endpoint_permissions \
    import RESTAPIEndpointPermissions
from rest_api_generator.rest_api_response import RESTAPIResponse
from rest_api_generator.rest_api_json_encoder import RESTAPIJSONEncoder
# ---------------------------------------------------------------------
