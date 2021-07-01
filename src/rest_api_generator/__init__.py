"""
    The api_generator package can be used to create a REST API for
    Flask by using classes to specify a API group.
"""
# ---------------------------------------------------------------------
# Imports
from rest_api_generator.rest_api_generator import RESTAPIGenerator, \
    BasicAuthorization, BearerAuthorzation
from rest_api_generator.endpoint import RESTAPIEndpoint
from rest_api_generator.group import RESTAPIGroup
from rest_api_generator.endpoint_url import RESTAPIEndpointURL
from rest_api_generator.authorization import RESTAPIAuthorization
from rest_api_generator.endpoint_scopes \
    import RESTAPIEndpointScopes
from rest_api_generator.response import RESTAPIResponse, ResponseType
from rest_api_generator.json_encoder import RESTAPIJSONEncoder
# ---------------------------------------------------------------------
